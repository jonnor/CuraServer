
function meshFromPolygon(polygon, xoffset, yoffset) {
    var geometry = new THREE.Geometry();

    // Generate the vertices of the n-gon.
    for (var i = 0; i < polygon.length; i++) {
        var p = polygon[i];
        console.log(p.length);
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
    if (obj) {
        obj.rotation.y += 0.01;
    }
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

    camera.position.z = 50;

    var req = new XMLHttpRequest();
    req.onload = function () {
        // HACK: polygons are given in global space, but we dont know the center. Hardcoded offset
        var xoffset = 100;
        var yoffset = 100;

        var polygons = JSON.parse(this.responseText);
        obj = new THREE.Object3D();
        for (var i=0; i<polygons.length; i++) {
            var item = polygons[i]['inset0'][0];
            console.log(item);
            var mesh = meshFromPolygon(item, xoffset, yoffset);
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

