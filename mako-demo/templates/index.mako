<%inherit file="base.mako"/>
<%namespace file="_price_tag.mako" import="price_tag"/>

<%def name="title()">${page_title} — Mako Demo</%def>

<h1>${page_title.upper()}</h1>

<ul class="products">
% for product in products:
    <li>
        <a href="/products/${product['id']}">${product['name']}</a>
        ${price_tag(product)}
    </li>
% endfor
% if not products:
    <li>No products yet.</li>
% endif
</ul>
