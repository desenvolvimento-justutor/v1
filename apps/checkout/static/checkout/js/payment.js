/* CREDIT CARD
 ===========================
 */
var card = new Card({
    // a selector or DOM element for the form where users will
    // be entering their information
    form: 'form', // *required*
    // a selector or DOM element for the container
    // where you want the card to appear
    container: '.card-wrapper', // *required*

    formSelectors: {
        numberInput: 'input[name="card_number"]', // optional — default input[name="number"]
        expiryInput: 'input[name="expiry_date"]', // optional — default input[name="expiry"]
        cvcInput: 'input[name="code"]', // optional — default input[name="cvc"]
        nameInput: 'input[name="name_on_card"]' // optional - defaults input[name="name"]
    },

    formatting: true, // optional - default true

    // Strings for translation - optional
    messages: {
        validDate: 'válido\naté', // optional - default 'valid\nthru'
        monthYear: 'mm/yy', // optional - default 'month/year'
    },

    // Default placeholders for rendered fields - optional
    placeholders: {
        number: '•••• •••• •••• ••••',
        name: 'NOME',
        expiry: '••/••',
        cvc: '•••'
    },

    masks: {
        cardNumber: '•' // optional - mask card number
    },

    // if true, will log helpful messages for setting up Card
    debug: true // optional - default false
});
