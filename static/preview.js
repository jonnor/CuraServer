
var controls, renderer, scene, camera;

function animate() {
   requestAnimationFrame(animate);
   controls.update();
}

function render() {
    renderer.render(scene, camera);
}

function init() {
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000 );
    renderer = new THREE.WebGLRenderer(); renderer.setSize( window.innerWidth, window.innerHeight );
    document.body.appendChild(renderer.domElement);
    controls = new THREE.OrbitControls(camera);
    controls.addEventListener('change', render)

    var geometry = new THREE.BoxGeometry(1,1,1);
    var material = new THREE.MeshBasicMaterial( { color: 0x00ff00 } );
    var cube = new THREE.Mesh( geometry, material ); scene.add( cube );
    camera.position.z = 5;

    render();
}
init();
