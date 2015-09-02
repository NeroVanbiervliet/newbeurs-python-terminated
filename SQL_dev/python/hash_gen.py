import bcrypt
password = b"guikwwdplnvccbsitkhr"
hashed = bcrypt.hashpw(password, bcrypt.gensalt())
print hashed
