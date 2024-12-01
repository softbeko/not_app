// Filtreleme fonksiyonu
function filterByCategory(categoryId) {
    var notes = document.querySelectorAll('.note'); // Tüm notları seç

    notes.forEach(function(note) {
        var noteCategory = note.getAttribute('data-category'); // Notun kategorisi

        // Kategoriyi karşılaştır
        if (categoryId === 'all' || noteCategory === categoryId) {
            note.style.display = 'table-row'; // Notu göster
        } else {
            note.style.display = 'none'; // Notu gizle
        }
    });
}
