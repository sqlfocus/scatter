#!/usr/bin/env python3
#! -*- coding: utf-8 -*-

import click      #pip3 install click

'''
@click.command()
@click.option("--username", type=str, help="arg for username", required=True)
@click.option("--passwd", type=str, help="arg for passwd")
def main(username, passwd):
    """
    python3 arg.py --help
    python3 arg.py --username lsq
    python3 arg.py --username=lsq --passwd=0123
    """
    print(f"{username}: {passwd}")

if __name__ == "__main__":
    main()
'''



@click.command()
@click.option("--old", type=click.Choice(['True', 'False']), help="is old main")
@click.option("--pos", nargs=2, type=int)
@click.option('--digit', type=click.IntRange(0, 10))
@click.argument("name")
def test(old, name, pos):
    '''--pos 1 2'''
    '''--pos=1 2'''
    print(f"{name} is {old}")
    print(f"{pos}")

@click.command()
@click.option("--username", type=str, help="arg for username", required=True)
@click.option("--passwd", type=str, help="arg for passwd", default="123")
def login(username, passwd):
    print(f"{username}: {passwd}")

    
@click.group()
def main():
    pass
main.add_command(login)
main.add_command(test)

if __name__ == "__main__":
    '''
    python3 arg.py --help
    python3 arg.py login --help
    '''
    main()


