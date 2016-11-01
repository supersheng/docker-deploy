from docker import Client
import os

app_parent_path = os.path.split(os.getcwd())[0]
app_path = app_parent_path + '/app'

class Container:
    def __init__(self):
        self.cli = Client(base_url='unix://var/run/docker.sock')

    def start(self, image, app_name='vote', app_path=app_path+'/vote', service_port=80):
        self.container = self.cli.create_container(
            image, name=app_name, ports=[service_port], volumes=['/app'],
            host_config = self.cli.create_host_config(binds={
                app_path: {
                    'bind': '/app',
                    'mode': 'rw',
                }
            })
        )
	app_container_id = self.container.get('Id')[:12]
        app_container_name = app_name+'_'+app_container_id

        self.cli.rename(app_container_id, app_container_name)
        self.cli.start(container=app_container_id)

        app_container_ip = self.cli.inspect_container(self.container.get('Id'))['NetworkSettings']['Networks']['bridge']['IPAddress']
	return app_container_ip
    
if __name__ == "__main__":
    print Container().start("tiangolo/uwsgi-nginx-flask")
