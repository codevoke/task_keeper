pattern = """ <strong>Hi, {username}!</strong><br>your email verification href: <a href="{url}/#{code}">click</a> """


def render_template(username: str, code: str, url: str) -> str:
    return pattern.format(username=username, code=code, url=url)
