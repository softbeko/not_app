$(document).ready(function(){
    $('.slider').slick({
        infinite: false,  // Sonsuz kaydırma
        slidesToShow: 1,  // Aynı anda 3 resim gösterilecek
        slidesToScroll: 1, // Bir kaydırmada 1 resim kayacak
        dots: true,  // Sayfalama noktaları aktif
        arrows: false,  // Sağ ve sol okları kaldır
        draggable: true, // Kaydırmayı aktif et
        swipeToSlide: true, // Kullanıcı kaydırmaya devam ettikçe bir sonraki slayta geç
        touchMove: true, // Mobilde sürükleyerek geçiş yapabilmeyi sağla
    });
});
