var map = L.map('map').setView([53.3498, -6.2603], 11); // Dublin

var openStreetMapLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: 'Map data © <a href="https://openstreetmap.org">OpenStreetMap</a> contributors'
});

openStreetMapLayer.addTo(map); 

var dublin1883 = L.geoJSON(null, {
  pointToLayer: function(feature, latlng) {
    var coordinates = feature.geometry.coordinates;
    var marker = L.marker([coordinates[0], coordinates[1]]).bindPopup('<h3>' + feature.properties.title + '</h3><p>' + feature.properties.text + '</p><img src="' + feature.properties.image + '">');
    return marker;
  }
});

var overlay2Layer = L.geoJSON(null, {
  pointToLayer: function(feature, latlng) {
    var coordinates = feature.geometry.coordinates;
    var marker = L.marker([coordinates[0], coordinates[1]]).bindPopup('<h3>' + feature.properties.title + '</h3><p>' + feature.properties.text + '</p><img src="' + feature.properties.image + '">');
    return marker;
  }
});

var markerLayerBase = L.layerGroup(); // create layer group for base map markers

$.getJSON('places.geojson', function(data) {
  data.features.forEach(function(feature) {
    var layerType = feature.properties.layerType; // now we need to put even more stuff in the geojson, yaaay....

    if (layerType === 'Dublin 1883') {
      dublin1883.addData(feature);
    } else if (layerType === 'Dublin 1904') {
      overlay2Layer.addData(feature);
    }

    // add markers to base map
    if (layerType === 'OpenStreetMap') {
      var coordinates = feature.geometry.coordinates;
      var marker = L.marker([coordinates[0], coordinates[1]]).bindPopup('<h3>' + feature.properties.title + '</h3><p>' + feature.properties.text + '</p><img src="' + feature.properties.image + '">');
      markerLayerBase.addLayer(marker);
    }
  });

  // initially show the dublin 1883 overlay with its markers
  map.addLayer(overlay); // add initial overlay to the map
  map.addLayer(dublin1883); // add marker layer group for Dublin 1883 to map
});

var point1 = L.latLng(53.36690, -6.30683),
  point2 = L.latLng(53.35956, -6.22052),
  point3 = L.latLng(53.32750, -6.31616),
  point4 = L.latLng(53.36945, -6.31796),
  point5 = L.latLng (53.3694, -6.21552),
  point6 = L.latLng (53.33332, -6.31977);


var overlay = L.imageOverlay.rotated("dublin1883.jpg", point1, point2, point3, {
  opacity: 1,
  interactive: true,
  attribution: "Historical building plan &copy; <a href='http://www.ign.es'>Instituto Geográfico Nacional de España</a>"
});


// in case we want to stick to the current overlay logic. the rest of the code should be easily adaptable in case we change it
var overlay2 = L.imageOverlay.rotated("Dublin1900.jpg", point4, point5, point6, {
  opacity: 1,
  interactive: true,
  attribution: "stuff for overlay 2"
});

var overlayMaps = {
  "Dublin 1883": overlay,
  "Overlay 2": overlay2
};

var baseMaps = {
  "OpenStreetMap": openStreetMapLayer,
};

L.control.layers(baseMaps, overlayMaps).addTo(map);

// event listener for overlayadd and overlayremove
map.on('overlayadd', function (eventLayer) {
  if (eventLayer.name === 'Dublin 1883') {
    map.removeLayer(markerLayerBase);
    map.addLayer(dublin1883);
  } else if (eventLayer.name === 'Overlay 2') {
    map.removeLayer(markerLayerBase);
    map.addLayer(overlay2Layer);
  }
});

map.on('overlayremove', function (eventLayer) {
  if (eventLayer.name === 'Dublin 1883') {
    map.removeLayer(dublin1883);
    map.addLayer(markerLayerBase);
  } else if (eventLayer.name === 'Overlay 2') {
    map.removeLayer(overlay2Layer);
    map.addLayer(markerLayerBase);
  }
});

// event listener to show/hide markers when using base layer
map.on('baselayerchange', function (eventLayer) {
  if (eventLayer.name === 'OpenStreetMap') {
    if (!map.hasLayer(overlay) && !map.hasLayer(overlay2)) {
      map.addLayer(markerLayerBase);
    }
  }
});
