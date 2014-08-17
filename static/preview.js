/*
In rough priority:
TODO: integrate into main page, with /preview URL
TODO: show the insetX polygons also
TODO: show print cost & time estimate
TODO: add UI for print settings, recalculate
TODO: show the gcode layers, allow to move up/down in interactively
TODO: show support and overhangs, using different colors
TODO: better interactive navigation
TODO: allow to rotate, scale objects in scene
TODO: show printer walls etc, for orientation. Should follow printer settings. Assets should be upstream?
*/

function meshFromPolygon(polygon, xoffset, yoffset) {
    var geometry = new THREE.Geometry();

    // Generate the vertices of the n-gon.
    for (var i = 0; i < polygon.length; i++) {
        var p = polygon[i];
        geometry.vertices.push(new THREE.Vector3(p[0]-xoffset, p[1]-yoffset, p[2]));
    }
    // Generate the faces of the n-gon.
    for (i = 0; i < polygon.length-2; i++) {
        geometry.faces.push(new THREE.Face3(0, i+1, i+2));
    }

    geometry.computeBoundingSphere();

    var material = new THREE.MeshBasicMaterial({color:"#ff0000"});
    var mesh = new THREE.Mesh(geometry, material);
    return mesh;
}

var controls, renderer, scene, camera, obj;

function animate() {
    requestAnimationFrame(animate);
    controls.update();
    render();
}

function render() {
    renderer.render(scene, camera);
}

function init() {
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000 );
    renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);

    controls = new THREE.OrbitControls(camera);
    controls.addEventListener('change', render)

    // TODO: set platform size based on settings
    var platformSizeX = 150;
    var platformSizeY = 150;
    var platformCenter = new THREE.Vector3(platformSizeX/2, platformSizeY/2, 0);

    var geometry = new THREE.BoxGeometry(platformSizeX,platformSizeY,1);
    var material = new THREE.MeshBasicMaterial( { color: 0xaaaaaa } );
    var platform = new THREE.Mesh(geometry, material);
    platform.position.x = platformCenter.x;
    platform.position.y = platformCenter.y;
    scene.add(platform);

    camera.position.y = -30;
    camera.position.x = platformCenter.x;
    camera.position.z = 100;
    controls.target = platformCenter;

    var req = new XMLHttpRequest();
    req.onload = function () {
        var polygons = JSON.parse(this.responseText);
        obj = new THREE.Object3D();
        for (var i=0; i<polygons.length; i++) {
            var item = polygons[i]['inset0'][0];
            var mesh = meshFromPolygon(item, 0, 0);
            obj.add(mesh);
        }

        scene.add(obj);
    }
    req.open("get", "polygons.json", true);
    req.send();

    animate();
    render();
}
init();

