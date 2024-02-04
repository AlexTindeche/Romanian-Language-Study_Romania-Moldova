with open('moldova/zugo_articles.txt', 'r') as f:
    file = f.read()
    file += "----------------------------------\n\n"

with open('moldova/zugo_articles.txt', 'w') as f:
    f.write(file)