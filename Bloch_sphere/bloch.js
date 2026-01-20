(function(){
  const canvas = document.getElementById('bloch');
  if (!canvas) return;

  // Renderer and scene
  const renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true });
  renderer.setPixelRatio(window.devicePixelRatio);

  const scene = new THREE.Scene();

  const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 100);
  camera.position.set(0, 0, 3);

  // Lights
  const amb = new THREE.AmbientLight(0xffffff, 0.7);
  scene.add(amb);
  const dir = new THREE.DirectionalLight(0xffffff, 0.6);
  dir.position.set(5, 5, 5);
  scene.add(dir);

  // Bloch sphere (wireframe)
  const sphereGeo = new THREE.SphereGeometry(1, 64, 64);
  const sphereMat = new THREE.MeshPhongMaterial({ color: 0xffffff, wireframe: true, opacity: 0.9 });
  const sphere = new THREE.Mesh(sphereGeo, sphereMat);
  scene.add(sphere);

  // Axes helper
  const axes = new THREE.AxesHelper(1.3);
  scene.add(axes);

  // Arrow helper - represents the state vector
  let arrow = new THREE.ArrowHelper(new THREE.Vector3(1,0,0), new THREE.Vector3(0,0,0), 1, 0x000000, 0.08, 0.05);
  scene.add(arrow);

  // Resize handling
  function resize() {
    const w = canvas.clientWidth || canvas.parentElement.clientWidth;
    const h = canvas.clientHeight || canvas.parentElement.clientHeight;
    if (!w || !h) return;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
  }
  window.addEventListener('resize', resize);
  resize();

  // Helpers to set the state
  function setState(thetaDeg, phiDeg) {
    // theta: polar angle from +Z (0..180), phi: azimuthal from X (0..360)
    const t = THREE.MathUtils.degToRad(thetaDeg);
    const p = THREE.MathUtils.degToRad(phiDeg);
    const x = Math.sin(t) * Math.cos(p);
    const y = Math.sin(t) * Math.sin(p);
    const z = Math.cos(t);
    const dirVec = new THREE.Vector3(x, y, z).normalize();

    // update arrow direction and length
    scene.remove(arrow);
    arrow = new THREE.ArrowHelper(dirVec, new THREE.Vector3(0,0,0), 1, 0x111111, 0.08, 0.05);
    scene.add(arrow);

    // update UI values
    const tval = document.getElementById('tval');
    const pval = document.getElementById('pval');
    if (tval) tval.textContent = String(thetaDeg);
    if (pval) pval.textContent = String(phiDeg);
  }

  // DOM bindings
  const theta = document.getElementById('theta');
  const phi = document.getElementById('phi');
  const btn0 = document.getElementById('btn0');
  const btn1 = document.getElementById('btn1');
  const randomBtn = document.getElementById('random');

  if (theta) theta.addEventListener('input', () => {
    setState(Number(theta.value), Number(phi.value));
  });
  if (phi) phi.addEventListener('input', () => {
    setState(Number(theta.value), Number(phi.value));
  });

  if (btn0) btn0.addEventListener('click', () => { if (theta) theta.value = 0; if (phi) phi.value = 0; setState(0,0); });
  if (btn1) btn1.addEventListener('click', () => { if (theta) theta.value = 180; if (phi) phi.value = 0; setState(180,0); });
  if (randomBtn) randomBtn.addEventListener('click', () => { const th = Math.floor(Math.random()*181); const ph = Math.floor(Math.random()*361); if (theta) theta.value = th; if (phi) phi.value = ph; setState(th,ph); });

  // simple auto-rotate for visibility
  let autoRotate = 0.002;
  function animate() {
    requestAnimationFrame(animate);
    sphere.rotation.y += autoRotate;
    renderer.render(scene, camera);
  }

  // initialize to default
  const initialTheta = theta ? Number(theta.value) : 90;
  const initialPhi = phi ? Number(phi.value) : 0;
  setState(initialTheta, initialPhi);
  animate();
})();