"""
This module to randomize passwords for your own or user's usages.
Supports for custom or default (8-16) lengths of passwords. Can be used
both as a standalone program or imported to your project.
    
Example:
    For default length:
    $ python3 password_randomizer.py
    For a variable length:
    $ python3 password_randomizer.py 20
    Note: if a variable length is not an integer, it would fallback 
    to either default length (if used as a standalone program) or
    0 if imported.
"""
import random, string, sys


list_of_symbols = list(string.ascii_letters + string.digits)

def check_int(num):
    """Check if arguement is integer.

    Arg:
        num (int): The only arguement.

    Returns:
        bool: The return value. True if num is indeed an integer, False otherwise.
    """
    if num is not None:
        try:
            int(num)
            return True
        except ValueError:
            return False
    else:
        return False


def randomize_password():
    """Randomizes password for default length, which is a 
    random range from 8 to 16.

    Returns:
        pswd (str): the string of password.
    """
    pswd = ""
    pswd_length = random.randrange(8, 17)
    for random_char in range(pswd_length):
        rnd = random.randrange(len(list_of_symbols))
        pswd += list_of_symbols[rnd]
    return pswd


def randomize_password_custom(length=0):
    """Randomizes password for variable length, which is by default 0.

    Returns:
        pswd (str): the string of password.
    """
    pswd = ""
    if check_int(length):
        for random_char in range(length):
            rnd = random.randrange(len(list_of_symbols))
            pswd += list_of_symbols[rnd]
        return pswd
    else:
        print("Length is not an int.")
        raise TypeError


def write_to_file(password="", txt="password.txt"):
    """Writes a string to the file. Passowrd and txt arguements,
    by default, are set to empty string and password.txt. Can be modified
    during call.

    Args:
        password (str): the string arguement.
        txt (str): the string arguement;
    
    """
    with open(txt, 'w') as f:
        f.write(password + "\n")

  
def main (length=None):
    """Main function to tie every part of module if it is used a standalone
    program. It checks the length if it was set, otherwise it is None. Then
    it randomizes the password and writes it to a file accordingly.
    """
    if check_int(length) and int(length) > 0:
        pswd = randomize_password_custom(int(length))
    else:
        print("Length wasn't recognized as a positive int, fallback to default randomizing.")
        pswd = randomize_password()
    write_to_file(pswd)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
