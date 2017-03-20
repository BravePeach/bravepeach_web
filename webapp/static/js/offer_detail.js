function randomRange(n1, n2) {
  return Math.floor( (Math.random() * (n2 - n1 + 1)) + n1 );
}

$(function () {
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
                zoom: 14,
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
