Django Pythonic Menu
--

This is a simple library to help with building and working with site menu in your way.

It solves one issue: list available menu items and toggle some of them active.
Then pass it to template. With menu levels if you wish. In readable way.

Usage is following:
```python
# 1. Define the menu
class AppMenu(Menu):
    first_menu_item = MenuItem('first_route')
    another_menu_item = MenuItem('another_route', title="Some title", and_other_value_passed_to_template='Yea!')

    class SubMenu(Menu):
        subitem = MenuItem('subitem_route')

        class Meta:
            visibility = lambda request, item: request.user.is_authenticated
            other_view_data = 'goes here'

# 2. Then activate it:
@AppMenu.first_menu_item.activate
def my_view(request):
    pass
```

```html
# 3. Then render it in view as you like it:
{% load pythonic_menu %}
{% render_menu 'path.to.AppMenu' menu %}

{% for item in menu.items %}
<a href="{{ item.url }}" {% if item.active %}class="active"{% endif %}>{{ item.title }}
{{ item.and_other_value_passed_to_template }}</a>
{% endfor %}
```
Extra abilities:
==
* Submenus (just define another Menu inside Menu).
* Visibility checking (provide `visibility=lambda request, item: request.user.is_staff` argument).
* Ability to provide callbacks for urls (just pass `callback(request, item)`).
* Ability to cache & validate routes (call `Menu.cache_routes()` in your `App.ready()` method.

Goals
==
Main goals are:
* This is static menu written in Python. So no models/DB.
* Simple way to be mark active items. Just add decorator to your views. Also it's bound to menu definition so existence of items is checked on app start.
* No restrictions on view: you have {url: , title: , active: ) from library. Everything other is yours: add icon=.., className=.. etc as you like.
* Rendering menu is project-specific so it's your responsibility to make template for it.

Feedback
==
If you have any ideas/questions post either issue or pull request.

If you use it and found useful then write me a message or make a pull request to change alter this page.
