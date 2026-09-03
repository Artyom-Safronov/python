<%inherit file="base.mako"/>
<%namespace file="_price_tag.mako" import="price_tag"/>

<%def name="title()">${product['name'] if product else 'Not found'}</%def>

% if product:
    <h1>${product['name']}</h1>
    ${price_tag(product)}

    % if related:
        <h2>Related</h2>
        <ul>
        % for item in related:
            <li>${item['name']}</li>
        % endfor
        </ul>
    % endif
% else:
    <p>Product not found.</p>
% endif
