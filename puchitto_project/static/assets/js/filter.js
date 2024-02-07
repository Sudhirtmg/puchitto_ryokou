$(document).ready(function (){
    $(".filter-checkbox").on("click", function(){
        console.log("A checkbox have been clicked");

        let filter_object = {}


 

        $(".filter-checkbox").each(function(){
            let filter_value = $(this).val()
            let filter_key = $(this).data("filter") // vendor, category

            console.log("Filter value is:", filter_value);
            console.log("Filter key is:", filter_key);

            filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter=' + filter_key + ']:checked')).map(function(element){
                return element.value
            })  
        })
        console.log("Filter Object is: ", filter_object);
        $.ajax({
            url: '/filter-packages',
            data: filter_object,
            dataType: 'json',
            beforeSend: function(){
                console.log("Trying to filter product...");
            },
            success: function(response){
                console.log(response.length);
                console.log("Data filtred successfully...");
                $(".totall-product").hide()
                $("#filtered-product").html(response.data)
            }
        })
    })

   
    $(document).on("submit", "#contact-form-ajax", function(e){
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
            dataType:"json",
            beforeSend: function(){
                console.log("Sending Data to Server...");
            },
            success: function(res){
                console.log("Sent Data to server!");
                $(".contact_us_p").hide()
                $("#contact-form-ajax").hide()
                $("#message-response").html("メッセージを送りました。")
            }
        })
    })

           


})