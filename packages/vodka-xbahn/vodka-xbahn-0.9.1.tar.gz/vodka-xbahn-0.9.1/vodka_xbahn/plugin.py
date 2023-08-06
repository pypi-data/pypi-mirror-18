import xbahn.api
import xbahn.connection

import vodka
import vodka.plugins
import vodka.config

class ConnectionConfiguration(vodka.config.Handler):
    name = vodka.config.Attribute(
        str,
        help_text="connection name"
    )
    bind = vodka.config.Attribute(
        str,
        default="",
        help_text="bind to this xbahn address (listen) - either 'bind' or 'connect' must be set"
    )
    connect = vodka.config.Attribute(
        str,
        default="",
        help_text="connect to this xbahn address (connect) - either 'connect' or 'bind' must be set"
    )


@vodka.plugin.register('xbahn')
class Xbahn(vodka.plugins.PluginBase):

    class Configuration(vodka.plugins.PluginBase.Configuration):
        connections = vodka.config.Attribute(
            list,
            help_text="xbahn connections",
            handler=lambda x,y: ConnectionConfiguration
        )

    def init(self):
        self.connections = {}
        self.links = {}
        self.connect()
        self.wire()

    def connect(self):
        for conn_cfg in self.get_config("connections"):
            name = conn_cfg.get("name")
            if "bind" in conn_cfg:
                self.connections[name] = xbahn.connection.listen(conn_cfg.get("bind"))
            elif "connect" in conn_cfg:
                self.connections[name] = xbahn.connection.connect(conn_cfg.get("connect"))
            self.connections[name].config=conn_cfg

    def wire(self):
        self.link = xbahn.connection.link.Link()

        for name, conn in self.connections.items():
            kwargs = { "receive" : conn }
            if conn.can_respond:
                kwargs.update(respond=conn)
            if conn.can_send:
                kwargs.update(send=conn)
            kwargs.update(meta=conn.config.get("meta",{}))
            self.link.wire(
                name,
                **kwargs
            )
        self.link.on("receive", self.on_receive)

    def disconnect(self):
        for name, conn in self.connections.items():
            conn.destroy()

    def on_receive(self, message=None, wire=None, event_origin=None):
        vodka.data.handle(
            "%s.%s" % (self.name, message.path),
            message.data,
            data_id=None,
            caller=self
        )
        print(message, self.name, message.path)
