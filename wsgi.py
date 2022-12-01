GROUP = 1
if GROUP == 1:
    from bol import app
if __name__ == '__main__':
    # print(*app.config.items(), sep='\n')
    # print('sadf')
    app.run(debug=True)