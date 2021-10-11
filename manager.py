import click
from app import db
from app.app_instance import app
from app.modules.users.models import User
from app.database.roles import UserType


@click.group()
def cli():
    pass


@click.command()
@click.option('--username')
@click.option('--password')
@click.option('--email')
@click.option('--first_name', default='',)
@click.option('--last_name', default='')
@click.option('--admin', default=False, is_flag=True)
def create_user(username, password, email, first_name, last_name, admin):
    with app.app_context():
        user = User(username=username, email=email, password=password,
                    first_name=first_name, last_name=last_name)
        if admin:
            user.role = UserType.ADMIN.value

        db.session.add(user)
        db.session.commit()

#
# @click.command()
# @click.option('--name')
# def create_role(name):
#     with app.app_context():
#         role = Role(name=name)
#         db.session.add(role)
#         db.session.commit()


@click.command()
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@click.command()
@click.argument('host', default='0.0.0.0')
@click.argument('port', default=5000)
@click.option('--debug', default=False, is_flag=True)
def runserver(host, port, debug):
    app.run(host=host, port=port, debug=debug)


cli.add_command(create_user)
# cli.add_command(create_role)
cli.add_command(recreate_db)
cli.add_command(runserver)

if __name__ == '__main__':
    cli()
