from sys import exit
import random

spaces ="                  "

bars = "______________________________________________________________"

title="""
 ██████╗░██╗░░░██╗███╗░░██╗░██████╗░███████╗░█████╗░███╗░░██╗░██████╗
 ██╔══██╗██║░░░██║████╗░██║██╔════╝░██╔════╝██╔══██╗████╗░██║██╔════╝
 ██║░░██║██║░░░██║██╔██╗██║██║░░██╗░█████╗░░██║░░██║██╔██╗██║╚█████╗░
 ██║░░██║██║░░░██║██║╚████║██║░░╚██╗██╔══╝░░██║░░██║██║╚████║░╚═══██╗
 ██████╔╝╚██████╔╝██║░╚███║╚██████╔╝███████╗╚█████╔╝██║░╚███║██████╔╝
 ╚═════╝░░╚═════╝░╚═╝░░╚══╝░╚═════╝░╚══════╝░╚════╝░╚═╝░░╚══╝╚═════╝░
"""

middle="""
                            ███╗░░██╗
                            ████╗░██║
                            ██╔██╗██║
                            ██║╚████║
                            ██║░╚███║
                            ╚═╝░░╚══╝
"""

tittle2="""
 ██████╗░██╗░░░██╗████████╗██╗░░██╗░█████╗░███╗░░██╗░██████╗
 ██╔══██╗╚██╗░██╔╝╚══██╔══╝██║░░██║██╔══██╗████╗░██║██╔════╝
 ██████╔╝░╚████╔╝░░░░██║░░░███████║██║░░██║██╔██╗██║╚█████╗░
 ██╔═══╝░░░╚██╔╝░░░░░██║░░░██╔══██║██║░░██║██║╚████║░╚═══██╗
 ██║░░░░░░░░██║░░░░░░██║░░░██║░░██║╚█████╔╝██║░╚███║██████╔╝
 ╚═╝░░░░░░░░╚═╝░░░░░░╚═╝░░░╚═╝░░╚═╝░╚════╝░╚═╝░░╚══╝╚═════╝░
"""

ea="""
    █░░ ▄▀█ ▀█ █▄█
    █▄▄ █▀█ █▄ ░█░

        █▀█ █▀█ █▀█ █▀▄ █░█ █▀▀ ▀█▀ █ █▀█ █▄░█ █▀
        █▀▀ █▀▄ █▄█ █▄▀ █▄█ █▄▄ ░█░ █ █▄█ █░▀█ ▄█
"""

end="""

 ████████╗██╗░░██╗███████╗  ███████╗███╗░░██╗██████╗░
 ╚══██╔══╝██║░░██║██╔════╝  ██╔════╝████╗░██║██╔══██╗
 ░░░██║░░░███████║█████╗░░  █████╗░░██╔██╗██║██║░░██║
 ░░░██║░░░██╔══██║██╔══╝░░  ██╔══╝░░██║╚████║██║░░██║
 ░░░██║░░░██║░░██║███████╗  ███████╗██║░╚███║██████╔╝
 ░░░╚═╝░░░╚═╝░░╚═╝╚══════╝  ╚══════╝╚═╝░░╚══╝╚═════╝░
"""

gameovertext="""
 ░██████╗░░█████╗░███╗░░░███╗███████╗
 ██╔════╝░██╔══██╗████╗░████║██╔════╝
 ██║░░██╗░███████║██╔████╔██║█████╗░░
 ██║░░╚██╗██╔══██║██║╚██╔╝██║██╔══╝░░
 ╚██████╔╝██║░░██║██║░╚═╝░██║███████╗
 ░╚═════╝░╚═╝░░╚═╝╚═╝░░░░░╚═╝╚══════╝
 
 ░█████╗░██╗░░░██╗███████╗██████╗░
 ██╔══██╗██║░░░██║██╔════╝██╔══██╗
 ██║░░██║╚██╗░██╔╝█████╗░░██████╔╝
 ██║░░██║░╚████╔╝░██╔══╝░░██╔══██╗
 ╚█████╔╝░░╚██╔╝░░███████╗██║░░██║
 ░╚════╝░░░░╚═╝░░░╚══════╝╚═╝░░╚═╝
"""