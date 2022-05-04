var config = {
	shop: 'http://multinity.com/',
	currency: {
		decimal: 2,
		prefix: 'R$ ',
		position: 'left', // prefix positioning
		onload: false, // formatting onload
		selector: '[data-price]'
	},
	calculate: {
		wrapper: '[data-calculate-me]',
		item: '.total-item',
		except: '.total',
		order: '#total-order',
		shipping: '#total-shipping',
		discount: '#total-discount',
		tax: '#total-tax',
		total: '#total-all'
	}
};