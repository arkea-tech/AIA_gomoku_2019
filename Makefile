##
## EPITECH PROJECT, 2018
## Makefile
## File description:
##
##

NAME = pbrain-gomoku-ai

SRC = pbrain-minMax.py

all		: 
		cp $(SRC) $(NAME)
		chmod +x $(NAME)

clean	: 
		rm -f $(NAME)

fclean	:	clean

re	:	fclean all

.PHONY	:	all clean fclean re
