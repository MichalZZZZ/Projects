document.addEventListener('DOMContentLoaded', function () {
    const nav = document.querySelector('.navbar');
    const allNavItems = document.querySelectorAll('.nav-link');
    const navList = document.querySelector('.navbar-collapse');

    function addShadow() {
        if (window.scrollY >= 100) {
            nav.classList.add('shadow-bg');
        } else {
            nav.classList.remove('shadow-bg');
        }
    }

    allNavItems.forEach(item => item.addEventListener('click', () => {
        navList.classList.remove('show')
    }))

    window.addEventListener('scroll', addShadow);
});



var owner = $('#owner'),
    cardNumber = $('#cardNumber'),
    cardNumberField = $('#card-number-field'),
    CVV = $("#cvv"),
    mastercard = $("#mastercard"),
    confirmButton = $('#confirm-purchase'),
    visa = $("#visa"),
    amex = $("#amex");


cardNumber.keyup(function() {
    amex.removeClass('transparent');
    visa.removeClass('transparent');
    mastercard.removeClass('transparent');

    if ($.payform.validateCardNumber(cardNumber.val()) == false) {
        cardNumberField.removeClass('has-success');
        cardNumberField.addClass('has-error');
    } else {
        cardNumberField.removeClass('has-error');
        cardNumberField.addClass('has-success');
    }

    if ($.payform.parseCardType(cardNumber.val()) == 'visa') {
        mastercard.addClass('transparent');
        amex.addClass('transparent');
    } else if ($.payform.parseCardType(cardNumber.val()) == 'amex') {
        mastercard.addClass('transparent');
        visa.addClass('transparent');
    } else if ($.payform.parseCardType(cardNumber.val()) == 'mastercard') {
        amex.addClass('transparent');
        visa.addClass('transparent');
    }
});

confirmButton.click(function(e) {
    e.preventDefault();

    var isCardValid = $.payform.validateCardNumber(cardNumber.val());
    var isCvvValid = $.payform.validateCardCVC(CVV.val());

    if(owner.val().length < 5){
        alert("Wrong owner name");
    } else if (!isCardValid) {
        alert("Wrong card number");
    } else if (!isCvvValid) {
        alert("Wrong CVV");
    } else {
        // Everything is correct. Add your form submission code here.
        alert("Everything is correct");
    }
});
