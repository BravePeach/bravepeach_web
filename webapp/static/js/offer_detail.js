// slider
var slideIndex = 1;

function plusSlides(n) {
  showSlides(slideIndex += n);
}

function currentSlide(n) {
  showSlides(slideIndex = n);
}

function showSlides(n) {
  var i;
  var slides = document.getElementsByClassName("mySlides");
  if (slides) {
      if (n > slides.length) {
          slideIndex = 1
      }
      if (n < 1) {
          slideIndex = slides.length
      }
      for (i = 0; i < slides.length; i++) {
          slides[i].style.display = "none";
      }
      slides[slideIndex - 1].style.display = "block";
  }
}

function randomRange(n1, n2) {
  return Math.floor( (Math.random() * (n2 - n1 + 1)) + n1 );
}

function addComment() {
    $.ajax({
        url: "/add_comment/",
        type: "POST",
        data: {
            user_id: document.getElementById("user_id").value,
            offer_id: document.getElementById("offer_id").value,
            content: $(".comment-form").val(),
        },
        success: function(c){
            $('.comment-form').val('');
            var newComment = '<div class="comment-inside-wrapper" style="display: none">' +
                        '<pre class="comment-user">' + c.content +
                        '</pre>' +
                    '</div>' +
                        '<div class="comment-time-user">' + c.created_at +
                        '</div>';

            $('.comment-inside-wrapper2').last().append(newComment);
            $('.comment-inside-wrapper').fadeIn('slow');
        }
    })
}

function openTerms(){
    var isOpened = $('.terms').css('display') == 'block';
    var isChecked = $('.checkbox').is(':checked');
    if(!isOpened && !isChecked){
        $('.terms').show('slow')
    }

    else if(isOpened && !isChecked){
        alert("여행자 약관에 동의해주세요")
    }

    else {
        console.log("thanks")
    }
}

function closeTerms(){
    $('.terms').hide('slow')
}

function fixButton() {
    var container = $('.button-wrapper');
    var maxTop = $('footer').offset().top - container.outerHeight() - 222;
    var scrollVal = $(document).scrollTop() + $(window).height() - 223;

    if (scrollVal > maxTop) {
        container.css('top', maxTop);
    }

    else {
        container.stop().animate({top: scrollVal},'100');
    }
}


$(function () {
    showSlides(slideIndex);
    fixButton();
    $('.button-wrapper').fadeIn('slow');
    $(document).scroll(function() {
        fixButton();
    });

    $('.map').each(function (index, Element) {
            var coords = $(Element).text().split(" ");
            var latlng = new google.maps.LatLng(parseFloat(coords[0]), parseFloat(coords[1]));

            Number.prototype.toRad = function () {
                return this * Math.PI / 180;
            };

            Number.prototype.toDeg = function () {
                return this * 180 / Math.PI;
            };

            google.maps.LatLng.prototype.destinationPoint = function (brng, dist) {
                dist = dist / 6371;
                brng = brng.toRad();

                var lat1 = this.lat().toRad(), lon1 = this.lng().toRad();

                var lat2 = Math.asin(Math.sin(lat1) * Math.cos(dist) +
                    Math.cos(lat1) * Math.sin(dist) * Math.cos(brng));

                var lon2 = lon1 + Math.atan2(Math.sin(brng) * Math.sin(dist) *
                        Math.cos(lat1),
                        Math.cos(dist) - Math.sin(lat1) *
                        Math.sin(lat2));

                if (isNaN(lat2) || isNaN(lon2)) return null;

                return new google.maps.LatLng(lat2.toDeg(), lon2.toDeg());
            };

            var randomBring = randomRange(0, 359);
            var randomDist = randomRange(0, 2) / 10;
            var newLatlng = latlng.destinationPoint(randomBring, randomDist);

            var myOptions = {
                zoom: 15,
                center: newLatlng,
                mapTypeId: google.maps.MapTypeId.ROADMAP,
                disableDefaultUI: false,
                mapTypeControl: true,
                zoomControl: true,
                zoomControlOptions: {
                    style: google.maps.ZoomControlStyle.SMALL
                }
            };

            var map = new google.maps.Map(Element, myOptions);

            var circle = new google.maps.Circle({
                center: newLatlng,
                map: map,
                strokeWeight: 0,
                fillColor: '#FF0000',
                fillOpacity: 0.35,
                radius: 200,
            });
        }
    );
});
