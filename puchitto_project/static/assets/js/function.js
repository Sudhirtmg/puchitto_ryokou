const monthNames = ["Jan", "Feb", "Mar", "April", "May", "June",
  "July", "Aug", "Sept", "Oct", "Nov", "Dec"
];

$('#commentForm').submit(function (e) {
    e.preventDefault();
    let dt = new Date();
    let time = dt.getDay() + " " + monthNames[dt.getUTCMonth()] + ", " + dt.getFullYear()
    $.ajax({
        data: $(this).serialize(),
        method: $(this).attr('method'),
        url: $(this).attr('action'),
        dataType: 'json',
        success: function (response) {
            console.log('保存しました');
            if(response.bool == true){

                $('#review-res').html('added')
                $('.hide-comment-form').hide()
                $('.add-review').hide()
                
                let _html= '<div class="single-comment justify-content-between d-flex mb-30" >'
                    _html +='<div class="user justify-content-between d-flex">'
                    _html += '<div class="thumb text-center">'
                    _html +=  '<img src="https://isobarscience-1bfd8.kxcdn.com/wp-content/uploads/2020/09/default-profile-picture1.jpg" alt="" />'
                    _html += '<a href="#" class="font-heading text-brand">'+ response.context.user +'</a>'
                    _html += ' </div>'
                    _html +='<div class="desc">'
                    _html +='<div class="d-flex justify-content-between mb-10">'
                    _html += '<div class="d-flex align-items-center">'
                    _html += '<span class="font-xs text-muted">'+ time +' </span>'
                    _html +='</div>'
                    
                    for(let i=1; i<=response.context.rating; i++){
                        _html += '<i class="fas fa-star text-warning"></i>'
                    }
                    _html +=' </div>'
                    _html += '<p class="mb-10">'+ response.context.review + '</p>'
                    _html += '</div>'
                    _html +='</div>'
                    _html += '</div >'
                    $(".comment-list").prepend(_html)
                }
                    
                }
    })
})

$(".add-to-cart-btn").on("click", function(){
    
    let this_val = $(this)
    let index = this_val.attr("data-index")

    let quantity = $(".product-quantity-" + index).val()
    let product_title = $(".product-title-" + index).val()

    let product_id = $(".product-id-" + index).val()
    let product_price = $(".current-product-price-" + index).text()

    let product_pid = $(".product-pid-" + index).val()
    let product_image = $(".product-image-" + index).val()


    console.log("Quantity:", quantity);
    console.log("Title:", product_title);
    console.log("Price:", product_price);
    console.log("ID:", product_id);
    console.log("PID:", product_pid);
    console.log("Image:", product_image);
    console.log("Index:", index);
    console.log("Currrent Element:", this_val);

    $.ajax({
        url: '/add-to-cart',
        data: {
            'id': product_id,
            'pid': product_pid,
            'image': product_image,
            'qty': quantity,
            'title': product_title,
            'price': product_price,
        },
        dataType: 'json',
        beforeSend: function(){
            console.log("予約しています。");
        },
        success: function(response){
            // this_val.html("✓")
            this_val.html("<i class='fas fa-check-circle'></i>")

            console.log("予約しました。");
            $(".cart-items-count").text(response.totalbookitems)


        }
    })
})



$(".delete-product").on("click", function(){
    
    let product_id = $(this).attr("data-product")
    let this_val = $(this)

    console.log("PRoduct ID:",  product_id);

    $.ajax({
        url: "/delete-from-cart",
        data: {
            "id": product_id
        },
        dataType: "json",
        beforeSend: function(){
            this_val.hide()
        },
        success: function(response){
            this_val.show()
            $(".cart-items-count").text(response.totalbookitems)
            $("#cart-list").html(response.data)
        }
    })

})


remove

$(".update-product").on("click", function(){
    
    let product_id = $(this).attr("data-product")
    let this_val = $(this)
    let product_quantity = $(".product-qty-"+product_id).val()

    console.log("PRoduct ID:",  product_id);
    console.log("PRoduct QTY:",  product_quantity);

    $.ajax({
        url: "/update-cart",
        data: {
            "id": product_id,
            "qty": product_quantity,
        },
        dataType: "json",
        beforeSend: function(){
            this_val.hide()
        },
        success: function(response){
            this_val.show()
            $(".cart-items-count").text(response.totalbookitems)
            $("#cart-list").html(response.data)
        }
    })

})

$(document).ready(function () {

    $(document).on("submit", "#contact-form-ajax", function (e) {
        e.preventDefault()
        console.log("Submited...");

        let full_name = $("#full_name").val()
        let email = $("#email").val()
        let phone = $("#phone").val()
        let subject = $("#subject").val()
        let message = $("#message").val()

        console.log("Name:", full_name);
        console.log("Email:", email);
        console.log("Phone:", phone);
        console.log("Subject:", subject);
        console.log("MEssage:", message);

        $.ajax({
            url: "/ajax-contact-form",
            data: {
                "full_name": full_name,
                "email": email,
                "phone": phone,
                "subject": subject,
                "message": message,
            },
            dataType: "json",
            beforeSend: function () {
                console.log("Sending Data to Server...");
            },
            success: function (res) {
                console.log("Sent Data to server!");
                $(".contact_us_p").hide()
                $("#contact-form-ajax").hide()
                $("#message-response").html("Message sent successfully.")
            }
        })
    })




})
