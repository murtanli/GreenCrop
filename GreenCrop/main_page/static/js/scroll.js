// Функция для проверки, находится ли элемент в пределах видимости
function isElementInViewport(el) {
    var rect = el.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}

// Функция для обработки прокрутки
function handleScroll() {
    var checkElement = document.querySelector('.block1');
    var header = document.querySelector('header');
    var links = document.querySelectorAll('.links a');

    if (isElementInViewport(checkElement)) {
        header.style.backgroundColor = 'rgba(144, 250, 179, 0.4)';

        links.forEach(function(link) {
            link.style.color = "black";
        });

        console.log('Пользователь долистал до элемента "check-element"');
    } else {
        links.forEach(function(link) {
            link.style.color = "white";
        });

        header.style.backgroundColor = 'transparent';
    }
}

// Функция для обработки изменения размера экрана
function handleResize() {
    // Здесь можно пересчитать позиции элементов или выполнить другие действия
    handleScroll(); // Обновить состояния при изменении размера экрана
}

// Установить слушатели событий
window.addEventListener('scroll', handleScroll);
window.addEventListener('resize', handleResize);

document.addEventListener('DOMContentLoaded', function() {
    var element = document.querySelector('header');
    var links = document.querySelectorAll('.links a');
    const scrollImage = document.getElementById('scrollImage');

    window.addEventListener('scroll', function() {
        var scrollPosition = window.scrollY || document.documentElement.scrollTop;

        var currentScrollY = window.scrollY;
        if (scrollPosition > 800) {
            links.forEach(function(link) {
                link.style.color = "black";
            });
            element.style.backgroundColor = 'rgba(144, 250, 179, 0.7)';
        } else if (scrollPosition < 400) {
            links.forEach(function(link) {
                link.style.color = "white";
            });
            element.style.backgroundColor = 'transparent';
        }
        if (scrollPosition < 200) {
            element.style.top = '0px';
        } else {
            element.style.top = '-4.5vh';
        }
        // if (currentScrollY > 1900 && currentScrollY < 4200) {
        //     element.style.backgroundColor = 'rgba(215,252,210, 0)';
        //     if (currentScrollY > 2900) {
        //         links.forEach(function(link) {
        //             link.style.color = "white";
        //         });
        //     }
        // }
    });
});

document.addEventListener('DOMContentLoaded', function() {

    document.getElementById('interface').addEventListener('click', function() {
        const targetElement = document.getElementById('block4');
        if (targetElement) {  
            targetElement.scrollIntoView({ behavior: 'smooth' });
        }
    });
    function scrollToElement(elementId) {
        const currentScrollY = window.scrollY || document.documentElement.scrollTop;
        const targetElement = document.getElementById(elementId);
        const viewportHeight = window.innerHeight;
        if (targetElement) {
            const yOffset = -currentScrollY - viewportHeight - 600; // Смещение по вертикали, если нужно
            console.log(`yoFFset - ${yOffset}`)
            const y = targetElement.getBoundingClientRect().top + window.pageYOffset + yOffset;
            window.scrollTo({ top: y, behavior: 'smooth' });
        }
    }

    // Добавление слушателя событий для ссылки регистрации в хедере
    try{
        document.getElementById('sign_in').addEventListener('click', function(event) {
        event.preventDefault();  
        scrollToElement('block5_auth_form');
        });
    } catch {
        
    }
    
    document.getElementById('about_us').addEventListener('click', function(event) {
        event.preventDefault();  
        scrollToElement('block6');
    });
    const scrollImage = document.getElementById('scrollImage');
    const img_right = document.getElementById('img_right');
    const img_left = document.getElementById('img_left');
    const block3_video = document.getElementById('block3_video');
    const block3_text_lines = document.getElementById('block3_text_lines');
    const block5_auth_form = document.getElementById('block5_auth_form');
    let lastScrollY = window.scrollY;

    window.addEventListener('scroll', function() {
        const currentScrollY = window.scrollY || document.documentElement.scrollTop;
        const viewportHeight = window.innerHeight;

        const triggerStart = viewportHeight * 2.3; // 2589px для адаптации к экрану
        const triggerEnd = viewportHeight * 3.5; // 3250px для адаптации к экрану
        
        const block4_Start = viewportHeight * 3;
        const block4_End = viewportHeight * 5.2;

        //console.log(currentScrollY);
        if (window.scrollY < 827 && window.scrollY > 400) {
            scrollImage.style.transform = `translateY(${-window.scrollY * 0.2 + 10}px)`;
        }
        if (window.scrollY < 1700 && window.scrollY > 900) {
            img_right.style.transform = `translateY(${(-window.scrollY * 0.4 + 20) + 450}px)`;
            img_left.style.transform = `translateY(${(-window.scrollY * 0.2 - 20) + 200}px)`;
        }

        if (currentScrollY > 1600 && currentScrollY < 2600) {
            block3_video.classList.add('block3_video_transition');
            block3_video.style.borderRadius = '1vh';
            block3_video.style.width = '100%';
            
            if (currentScrollY > 1700 && currentScrollY < 2600) {
                document.getElementById('text_moving').classList.remove('text_none');
                document.getElementById('text_moving').classList.add('overlay_wrapper');
                block3_video.classList.remove('block3_video_transition');
                block3_video.classList.add('block3_video_transition_fast');
                block3_video.style.transform = `translateY(${(currentScrollY / 100 - 10)}vh)`;
            }
        } 

        if (currentScrollY > triggerStart && currentScrollY < triggerEnd) {
            // block3_video.style.top = '1vh';
            block3_video.style.transform = `translateY(${(currentScrollY - triggerStart) / 100 + 15}vh)`;
            // block3_video.style.position = 'fixed';
            
            block3_text_lines.style.transform = `translateY(${(currentScrollY - triggerStart) / 100 + 15}vh)`;
            // block3_text_lines.style.position = 'fixed';
        }else {
            block3_video.style.width = '90%';
            block3_video.style.position = 'absolute';
            block3_video.style.borderRadius = '10vh';
        }
        const block4_block = this.document.getElementById('block4');

        if (currentScrollY > block4_Start && currentScrollY < block4_End){
            
            block4_block.classList.remove('block4_none');
            block4_block.classList.add('block4');

            
            block4_block.style.transform = `translateY(${(block4_Start - currentScrollY) / 10}vh)`;
            var header = document.querySelector('header');
            var links = document.querySelectorAll('.links a');
            
            const block4_img = this.document.getElementById('block4_imgs_id');
            const block4_img1 = document.getElementById('block4_img1_id');
            const block4_img2 = document.getElementById('block4_img2_id');
            const shadow_title = document.getElementById('shadow_title');
            const block5 = document.getElementById('block5');
            // block4_img.style.display = 'none';

            if (currentScrollY > (viewportHeight * 3.456) && currentScrollY < (viewportHeight * 4.7)) {
                links.forEach(function(link) {
                    link.style.color = "white";
                });
                header.style.backgroundColor = 'rgba(136,145,147, 0.2)';
            } else if (currentScrollY > (viewportHeight * 5)) {
                header.style.backgroundColor = 'none';
                header.style.display = 'none';
                header.style.transition = 'background-color 0.3s';
            } else {
                header.style.backgroundColor = 'rgba(136,145,147, 0.2)';
                header.style.display = 'flex';
                
            }

            if ( currentScrollY > (viewportHeight * 3.1) && currentScrollY < (viewportHeight * 4.3)){
                if (currentScrollY > (viewportHeight * 3.4) && currentScrollY < (viewportHeight * 4.1) ){
                    block4_img1.classList.add('active');
                    block4_img2.classList.add('active');
                    shadow_title.style.transform = `translateY(${((block4_Start - currentScrollY) / 40)}vh)`;
                    
                } else {
                block4_img1.classList.remove('active');
                block4_img2.classList.remove('active');
                block4_img1.classList.add('block4_img1');
                block4_img2.classList.add('block4_img2');
                        
                if (currentScrollY > (viewportHeight * 4) && currentScrollY < (viewportHeight * 4.7)){
                    block5_auth_form.classList.add('active');
                    block5.style.transform = `translateY(${(block4_Start - currentScrollY) / 50}vh)`;
                } else {
                    block5_auth_form.classList.remove('active');
                }
            }
        
            } 
        } else {
            //block4_block.style.display = 'none';
        
        }
        lastScrollY = currentScrollY;
    });
});
