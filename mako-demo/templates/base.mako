<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>${self.title()}</title>
</head>
<body>
    <%include file="_nav.mako"/>

    <main>
        ${self.body()}
    </main>

    <%include file="_footer.mako"/>
</body>
</html>

<%def name="title()">Mako Demo</%def>
