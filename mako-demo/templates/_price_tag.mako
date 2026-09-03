<%def name="price_tag(product)">
    <span class="price ${'in-stock' if product['in_stock'] else 'out-of-stock'}">
        ${'%.2f' % product['price']} USD
    </span>
</%def>
