window.addEventListener('load', function() {
    var prev = document.querySelector('.prev');
    var next = document.querySelector('.next');
    var lunbo = document.querySelector('.lunbo');
    var lunboWidth = lunbo.offsetWidth;
    lunbo.addEventListener('mouseenter', function() {
        prev.style.display = 'block';
        next.style.display = 'block';
        clearInterval(timer);
        timer = null;
    });
    lunbo.addEventListener('mouseleave', function() {
        prev.style.display = 'none';
        next.style.display = 'none';
        timer = setInterval(function() {
            next.click();
        }, 2000);
    });
    var bone = document.querySelector('.bone');
    var ol = document.querySelector('ol');
    for (var i = 0; i < bone.children.length; i++) {
        var li = document.createElement('li');
        li.setAttribute('index', i);
        ol.appendChild(li);
        li.addEventListener('click', function() {
            for (var i = 0; i < ol.children.length; i++) {
                ol.children[i].className = '';
            }
            this.className = 'current';
            var index = this.getAttribute('index');
            num = index;
            circle = index;
            animate(bone, -index * lunboWidth);
        });
    }
    ol.children[0].className = 'current';
    var num = 0;
    var circle = 0;
    var flag = true;
    next.addEventListener('click', function() {
        if (flag) {
            flag = false;
            if (num == bone.children.length - 1) {
                bone.style.left = 0;
                num = -1;
            }
            num++;
            animate(bone, -num * lunboWidth, function() {
                flag = true;
            });
            circle++;
            if (circle == ol.children.length) {
                circle = 0;
            }
            for (var i = 0; i < ol.children.length; i++) {
                ol.children[i].className = '';
            }
            ol.children[circle].className = 'current';
        }
    });
    prev.addEventListener('click', function() {
        if (flag) {
            flag = false;
            if (num == 0) {
                num = bone.children.length;
                bone.style.left = num * lunboWidth + 'px';
            }
            num--;
            animate(bone, -num * lunboWidth, function() {
                flag = true;
            });
            circle--;
            if (circle < 0) {
                circle = ol.children.length - 1;
            }
            for (var i = 0; i < ol.children.length; i++) {
                ol.children[i].className = '';
            }
            ol.children[circle].className = 'current';
        }
    });
    var timer = setInterval(function() {
        next.click();
    }, 2000);
});