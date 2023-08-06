from hashlib import sha1
from pika import BasicProperties
from rask.base import Base
from rask.rmq import Announce,BasicProperties
from .codec import dictfy,jsonify
from .cursor import Cursor

__all__ = ['Mongodb']

class Mongodb(Base):
    __queue = None
    __publish = None
    __request = None
    __options = None

    @property
    def __request__(self):
        try:
            assert self.__request
        except AssertionError:
            self.__request = {}
        except:
            raise
        return self.__request

    @property
    def etag(self):
        return sha1('%s:%s' % (self.uuid,self.ioengine.uuid4)).hexdigest()

    @property
    def options(self):
        try:
            assert self.__options
        except AssertionError:
            self.__options = {
                'rmq':{
                    'exchange':{
                        'topic':'njord_mongodb',
                        'headers':'njord_mongodb_headers'
                    },
                    'services':{
                        'response':{
                            'durable':False,
                            'exclusive':True,
                            'queue':'njord_mongodb_%s' % self.etag,
                            'bind_args':{
                                'mongodb-response':True,
                                'dogtag':self.uuid,
                                'x-match':'all'
                            }
                        }
                    }
                },
                'services':{
                    'aggregate':'njord.mongodb.aggregate.%s',
                    'cursor_close':'njord.mongodb.cursor.close.%s.%s',
                    'cursor_fetch':'njord.mongodb.cursor.fetch.%s.%s',
                    'find':'njord.mongodb.find.%s',
                    'find_and_modify':'njord.mongodb.find_and_modify.%s',
                    'find_one':'njord.mongodb.find_one.%s',
                    'insert':'njord.mongodb.insert.%s',
                    'remove':'njord.mongodb.remove.%s',
                    'save':'njord.mongodb.save.%s',
                    'update':'njord.mongodb.update.%s'
                }
            }
        except:
            raise
        return self.__options

    @property
    def publish(self):
        try:
            assert self.__publish
        except AssertionError:
            return None
        except:
            raise
        return self.__publish.basic_publish

    def __consumer__(self,_):
        def on(channel):
            channel.result().channel.basic_consume(
                consumer_callback=self.__on_msg__,
                queue=self.options['rmq']['services']['response']['queue']
            )
            self.__ready__('consumer')
            return True

        self.rmq.channel('mongodb_consumer_%s' % self.uuid,self.ioengine.future(on))
        return True

    def __cursor__(self,cluster,uid,cursor):
        return Cursor(
            cluster=cluster,
            uid=uid,
            cursor=cursor,
            fetch=self.cursor_fetch,
            close=self.cursor_close
        )

    def __execute__(self,body,rk,future,headers=None):
        etag = self.etag

        def on_response(result):
            try:
                result = dictfy(result.result())
                assert result['ok']
            except (AssertionError,KeyError):
                future.set_exception(ExecutionError(result.get('err')))
            except:
                raise
            else:
                future.set_result(result)
            return True

        self.__request__[etag] = self.ioengine.future(on_response)
        headers = headers or {}
        headers.update({
            'etag':etag,
            'dogtag':self.uuid
        })
        self.publish(
            body=body,
            exchange=self.options['rmq']['exchange']['topic'],
            routing_key=rk,
            properties=BasicProperties(headers=headers)
        )
        return True

    def __init__(self,rmq):
        self.rmq = rmq
        self.__wait__ = ['publish','consumer']
        self.ioengine.loop.add_callback(self.__services__)

    def __on_msg__(self,channel,method,properties,body):
        try:
            assert properties.headers['etag'] in self.__request__
        except (AssertionError,KeyError,TypeError):
            pass
        except:
            raise
        else:
            self.__request__[properties.headers['etag']].set_result(body)
            del self.__request__[properties.headers['etag']]

        channel.basic_ack(method.delivery_tag)
        return True

    def __queue_declare__(self,_):
        Announce(
            channel=_,
            settings=self.options['rmq'],
            future=self.ioengine.future(self.__consumer__)
        )
        return True

    def __ready__(self,_):
        try:
            self.__wait__.remove(_)
            self.log.info(_)
            assert not self.__wait__
        except (AssertionError,ValueError):
            pass
        except:
            raise
        else:
            self.active = True
        return True

    def __services__(self):
        def publish(channel):
            self.__publish = channel.result().channel
            self.__ready__('publish')
            return True

        self.rmq.channel('mongodb_announce_%s' % self.uuid,self.ioengine.future(self.__queue_declare__))
        self.rmq.channel('mongodb_publish_%s' % self.uuid,self.ioengine.future(publish))
        return True

    def aggregate(self,cluster,db,collection,future,**kwargs):
        try:
            assert self.active
        except AssertionError:
            def ready(_):
                self.ioengine.loop.add_callback(
                    self.aggregate,
                    cluster=cluster,
                    db=db,
                    collection=collection,
                    future=future,
                    **kwargs
                )
                return True

            self.promises.append(self.ioengine.future(ready))
        except:
            raise
        else:
            def on_cursor(_):
                try:
                    assert _.result()['cursor']
                except AssertionError:
                    future.set_result({
                        'doc':_.result()['doc'],
                        'cursor':None
                    })
                except ExecutionError as ex:
                    future.set_exception(ex)
                except:
                    raise
                else:
                    future.set_result({
                        'doc':_.result()['doc'],
                        'cursor':self.__cursor__(
                            cluster=cluster,
                            uid=_.result()['cursor']['uid'],
                            cursor=_.result()['cursor']['id']
                        )
                    })
                return True

            self.ioengine.loop.add_callback(
                self.__execute__,
                body=jsonify(kwargs),
                rk=self.options['services']['aggregate'] % cluster,
                headers={
                    'db':db,
                    'collection':collection
                },
                future=self.ioengine.future(on_cursor)
            )
        return True

    def cursor_close(self,cluster,uid,cursor):
        try:
            assert self.active
        except AssertionError:
            def ready(_):
                self.ioengine.lopp.add_callback(
                    self.cursor_close,
                    cluster=cluster,
                    uid=uid,
                    cursor=cursor
                )
                return True

            self.promises.append(self.ioengine.future(ready))
        except:
            raise
        else:
            self.publish(
                body=cursor,
                exchange=self.options['rmq']['exchange']['topic'],
                routing_key=self.options['services']['cursor_close'] % (cluster,uid)
            )
        return True

    def cursor_fetch(self,cluster,uid,cursor,future):
        try:
            assert self.active
        except AssertionError:
            def ready(_):
                self.ioengine.lopp.add_callback(
                    self.cursor_fetch,
                    cluster=cluster,
                    uid=uid,
                    cursor=cursor,
                    future=future
                )
                return True

            self.promises.append(self.ioengine.future(ready))
        except:
            raise
        else:
            def on_response(_):
                future.set_result(_.result())
                return True

            self.ioengine.loop.add_callback(
                self.__execute__,
                body=cursor,
                rk=self.options['services']['cursor_fetch'] % (cluster,uid),
                headers={},
                future=self.ioengine.future(on_response)
            )
        return True

    def find(self,cluster,db,collection,future,**kwargs):
        try:
            assert self.active
        except AssertionError:
            def ready(_):
                self.ioengine.loop.add_callback(
                    self.find,
                    cluster=cluster,
                    db=db,
                    collection=collection,
                    future=future,
                    **kwargs
                )
                return True

            self.promises.append(self.ioengine.future(ready))
        except:
            raise
        else:
            def on_cursor(_):
                try:
                    assert _.result()['cursor']
                except AssertionError:
                    future.set_result(_.result())
                except ExecutionError as ex:
                    future.set_exception(ex)
                except:
                    raise
                else:
                    future.set_result({
                        'doc':_.result()['doc'],
                        'cursor':self.__cursor__(
                            cluster=cluster,
                            uid=_.result()['cursor']['uid'],
                            cursor=_.result()['cursor']['id']
                        )
                    })
                return True

            self.ioengine.loop.add_callback(
                self.__execute__,
                body=jsonify(kwargs),
                rk=self.options['services']['find'] % cluster,
                headers={
                    'db':db,
                    'collection':collection
                },
                future=self.ioengine.future(on_cursor)
            )
        return True

    def find_and_modify(self,cluster,db,collection,future,**kwargs):
        try:
            assert self.active
        except AssertionError:
            def ready(_):
                self.ioengine.loop.add_callback(
                    self.find_and_modify,
                    cluster=cluster,
                    db=db,
                    collection=collection,
                    future=future,
                    **kwargs
                )
                return True

            self.promises.append(self.ioengine.future(ready))
        except:
            raise
        else:
            def on_find(_):
                try:
                    future.set_result(_.result()['doc'])
                except ExecutionError as ex:
                    future.set_exception(ex)
                except:
                    raise
                return True

            self.ioengine.loop.add_callback(
                self.__execute__,
                body=jsonify(kwargs),
                rk=self.options['services']['find_and_modify'] % cluster,
                headers={
                    'db':db,
                    'collection':collection
                },
                future=self.ioengine.future(on_find)
            )
        return True

    def find_one(self,cluster,db,collection,future,**kwargs):
        try:
            assert self.active
        except AssertionError:
            def ready(_):
                self.ioengine.loop.add_callback(
                    self.find_one,
                    cluster=cluster,
                    db=db,
                    collection=collection,
                    future=future,
                    **kwargs
                )
                return True

            self.promises.append(self.ioengine.future(ready))
        except:
            raise
        else:
            def on_find(_):
                try:
                    future.set_result(_.result()['doc'])
                except ExecutionError as ex:
                    future.set_exception(ex)
                except:
                    raise
                return True

            self.ioengine.loop.add_callback(
                self.__execute__,
                body=jsonify(kwargs),
                rk=self.options['services']['find_one'] % cluster,
                headers={
                    'db':db,
                    'collection':collection
                },
                future=self.ioengine.future(on_find)
            )
        return True

    def insert(self,cluster,db,collection,future,**kwargs):
        try:
            assert self.active
        except AssertionError:
            def ready(_):
                self.ioengine.loop.add_callback(
                    self.insert,
                    cluster=cluster,
                    db=db,
                    collection=collection,
                    future=future,
                    **kwargs
                )
                return True

            self.promises.append(self.ioengine.future(ready))
        except:
            raise
        else:
            def on_insert(_):
                try:
                    future.set_result(_.result()['_id'])
                except ExecutionError as ex:
                    future.set_exception(ex)
                except:
                    raise
                return True

            self.ioengine.loop.add_callback(
                self.__execute__,
                body=jsonify(kwargs),
                rk=self.options['services']['insert'] % cluster,
                headers={
                    'db':db,
                    'collection':collection
                },
                future=self.ioengine.future(on_insert)
            )
        return True

    def remove(self,cluster,db,collection,future,**kwargs):
        try:
            assert self.active
        except AssertionError:
            def ready(_):
                self.ioengine.loop.add_callback(
                    self.remove,
                    cluster=cluster,
                    db=db,
                    collection=collection,
                    future=future,
                    **kwargs
                )
                return True

            self.promises.append(self.ioengine.future(ready))
        except:
            raise
        else:
            def on_remove(_):
                try:
                    future.set_result(_.result()['result'])
                except ExecutionError as ex:
                    future.set_exception(ex)
                except:
                    raise
                return True

            self.ioengine.loop.add_callback(
                self.__execute__,
                body=jsonify(kwargs),
                rk=self.options['services']['remove'] % cluster,
                headers={
                    'db':db,
                    'collection':collection
                },
                future=self.ioengine.future(on_remove)
            )
        return True

    def save(self,cluster,db,collection,future,**kwargs):
        try:
            assert self.active
        except AssertionError:
            def ready(_):
                self.ioengine.loop.add_callback(
                    self.save,
                    cluster=cluster,
                    db=db,
                    collection=collection,
                    future=future,
                    **kwargs
                )
                return True

            self.promises.append(self.ioengine.future(ready))
        except:
            raise
        else:
            def on_save(_):
                try:
                    future.set_result(_.result()['_id'])
                except ExecutionError as ex:
                    future.set_exception(ex)
                except:
                    raise
                return True

            self.ioengine.loop.add_callback(
                self.__execute__,
                body=jsonify(kwargs),
                rk=self.options['services']['save'] % cluster,
                headers={
                    'db':db,
                    'collection':collection
                },
                future=self.ioengine.future(on_save)
            )
        return True

    def update(self,cluster,db,collection,future,**kwargs):
        try:
            assert self.active
        except AssertionError:
            def ready(_):
                self.ioengine.loop.add_callback(
                    self.update,
                    cluster=cluster,
                    db=db,
                    collection=collection,
                    future=future,
                    **kwargs
                )
                return True

            self.promises.append(self.ioengine.future(ready))
        except:
            raise
        else:
            def on_update(_):
                try:
                    future.set_result(_.result()['result'])
                except ExecutionError as ex:
                    future.set_exception(ex)
                except:
                    raise
                return True

            self.ioengine.loop.add_callback(
                self.__execute__,
                body=jsonify(kwargs),
                rk=self.options['services']['update'] % cluster,
                headers={
                    'db':db,
                    'collection':collection
                },
                future=self.ioengine.future(on_update)
            )
        return True

class ExecutionError(Exception):
    pass
