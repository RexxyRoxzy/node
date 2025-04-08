/*!
 * particles.js v2.0.0
 * https://github.com/VincentGarreau/particles.js
 *
 * Copyright (c) 2016 Vincent Garreau
 * Licensed under the MIT license
 */
!function(e,t){"object"==typeof exports&&"undefined"!=typeof module?module.exports=t():"function"==typeof define&&define.amd?define(t):e.ParticlesJS=t()}(this,function(){"use strict";function e(e,t){return t={exports:{}},e(t,t.exports),t.exports}var t=e(function(e,t){Object.defineProperty(t,"__esModule",{value:!0});var n=function(){function e(e,t){for(var n=0;n<t.length;n++){var i=t[n];i.enumerable=i.enumerable||!1,i.configurable=!0,"value"in i&&(i.writable=!0),Object.defineProperty(e,i.key,i)}}return function(t,n,i){return n&&e(t.prototype,n),i&&e(t,i),t}}();var i=function(){function e(t,n){var i=this;!function(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}(this,e),this.canvas=t,this.ctx=t.getContext("2d"),this.particlesArray=[],this.canvasWidth=t.width,this.canvasHeight=t.height,this.options=n,this.connectParticles=n.connectParticles||!1;var a=this.options.maxParticles||100;for(var r=0;r<a;r++)this.particlesArray.push(new Particle(this.canvas,this.options));this.animate=this.animate.bind(this),this.animate(),window.addEventListener("resize",function(){i.resize()},!1)}return n(e,[{key:"animate",value:function(){var e=this;this.ctx.clearRect(0,0,this.canvasWidth,this.canvasHeight),this.particlesArray.forEach(function(t,n){t.draw(),t.update(),e.connectParticles&&e.connect(t,e.particlesArray.slice(n))}),requestAnimationFrame(this.animate)}},{key:"connect",value:function(e,t){var n=this,i=this.options.connectDistance||100,a=this.options.connectLineWidth||1,r=this.options.connectLineColor||"#ffffff";t.forEach(function(t){var o=Math.sqrt(Math.pow(e.x-t.x,2)+Math.pow(e.y-t.y,2));if(o<i){var s=1-o/i;n.ctx.beginPath(),n.ctx.strokeStyle=r,n.ctx.lineWidth=s*a,n.ctx.moveTo(e.x,e.y),n.ctx.lineTo(t.x,t.y),n.ctx.stroke()}})}},{key:"resize",value:function(){var e=this;this.canvas.width=window.innerWidth,this.canvas.height=window.innerHeight,this.canvasWidth=this.canvas.width,this.canvasHeight=this.canvas.height,this.particlesArray.forEach(function(t){t.containerWidth=e.canvasWidth,t.containerHeight=e.canvasHeight})}}]),e}();var Particle=function(){function e(t,n){!function(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}(this,e),this.canvas=t,this.options=n,this.x=Math.random()*t.width,this.y=Math.random()*t.height,this.velocity={x:(Math.random()-.5)*n.speed||1,y:(Math.random()-.5)*n.speed||1},this.radius=n.particleRadius||3,this.color=n.particleColor||"#ffffff",this.containerWidth=t.width,this.containerHeight=t.height}return n(e,[{key:"update",value:function(){this.x+this.velocity.x+this.radius>this.containerWidth||this.x+this.velocity.x-this.radius<0?this.velocity.x=-this.velocity.x:this.y+this.velocity.y+this.radius>this.containerHeight||this.y+this.velocity.y-this.radius<0?this.velocity.y=-this.velocity.y:(this.x+=this.velocity.x,this.y+=this.velocity.y)}},{key:"draw",value:function(){var e=this.canvas.getContext("2d");e.beginPath(),e.arc(this.x,this.y,this.radius,0,2*Math.PI),e.fillStyle=this.color,e.fill()}}]),e}();t.default=i});return t.default});

/* Initialization function for particles.js */
function initParticles(containerId, options) {
    const defaults = {
        maxParticles: 120, // Number of particles
        particleRadius: 1.5, // Size of particles
        particleColor: '#000000', // Color of particles
        speed: 0.3, // Speed of particles
        connectParticles: true, // Connect particles with lines
        connectDistance: 140, // Maximum distance for connecting lines
        connectLineWidth: 0.5, // Line width for connections
        connectLineColor: '#000000' // Line color for connections
    };

    // Merge defaults with custom options
    const settings = Object.assign({}, defaults, options || {});
    
    // Get the container element
    const container = document.getElementById(containerId);
    if (!container) {
        console.error(`Container element with id "${containerId}" not found.`);
        return;
    }
    
    // Create the canvas element
    const canvas = document.createElement('canvas');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    container.appendChild(canvas);
    
    // Initialize particles
    new ParticlesJS(canvas, settings);
    
    // Adjust canvas size on window resize
    window.addEventListener('resize', function() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    });
}
