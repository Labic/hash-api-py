from japronto import Application
from resources import Article

app = Application()

app.router.add_route('/articles', Article.query, 'GET')
app.router.add_route('/articles/{id}', Article.lookup, 'GET')
app.router.add_route('/articles', Article.delete, 'DELETE')
app.router.add_route('/articles/{id}', Article.delete, 'DELETE')

app.run()