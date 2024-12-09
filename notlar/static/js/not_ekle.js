$(document).ready(function() {
    // Üniversiteleri almak için API'yi çağırıyoruz
    $.get('http://127.0.0.1:8000/api/universities/', function(data) {
        let universities = data.results; // API'den gelen üniversiteler

        // Üniversiteleri alfabetik sıraya göre sıralayın
        universities.sort(function(a, b) {
            return a.isim.localeCompare(b.isim, 'tr'); // Türkçe karakter desteği için 'tr'
        });

        // Üniversiteleri Select box'ına ekleyelim
        universities.forEach(function(university) {
            $('#university-select').append(
                `<option value="${university.kod}">${university.isim}</option>`
            );
        });
    });

    // Üniversite Seçildiğinde Bölümleri Al ve Göster
    $('#university-select').change(function() {
        const selectedUniversityId = $(this).val();
        if (selectedUniversityId) {
            // Seçilen üniversiteye ait bölümleri alıyoruz
            $.get(`http://127.0.0.1:8000/api/departments/?university_id=${selectedUniversityId}`, function(data) {
                const departments = data.results; // Bölümleri al

                // Eğer bölümler varsa, select'i doldur
                if (departments.length > 0) {
                    let departmentOptions = '<option value="">Bir bölüm seçin</option>';

                    // Bölümleri alfabetik sıraya göre sıralayın
                    departments.sort(function(a, b) {
                        return a.isim.localeCompare(b.isim, 'tr'); // Türkçe karakter desteği için 'tr'
                    });

                    // Bölümleri Select box'ına ekleyelim
                    departments.forEach(function(department) {
                        departmentOptions += `<option value="${department.id}">${department.isim}</option>`;
                    });
                    $('#department-select').html(departmentOptions);
                } else {
                    // Bölüm yoksa, "Bölüm Bulunamadı" yazısı ekleyelim
                    $('#department-select').html('<option value="">Bu üniversite için bölüm bulunamadı</option>');
                }
            });
        } else {
            // Üniversite seçilmediyse, bölüm select'ini temizle
            $('#department-select').html('<option value="">Bir bölüm seçin</option>');
        }
    });
});

$(function () {
    $("#id_kategori, #id_is_shared").change(function () {
        const isDers = $("#id_kategori").val() === "ders"; // "ders" seçimi kontrolü
        const isShared = $("#id_is_shared").prop('checked'); // Paylaşım durumu kontrolü
        
        // Dosya yükleme alanının zorunluluk durumu
        if (isDers && isShared) {
            $("#id_file").prop('required', true);  
        } else {
            $("#id_file").prop('required', false); 
        }

        // Ders kategorisine bağlı alanların görünürlüğü ve durumu
        $("#id_ders_kategori").closest(".mb-3").toggle(isDers);
        $("#id_ders_kategori").prop('disabled', !isDers);

        $(".form-check.mb-3").toggle(isDers);
        $("#id_is_shared").prop('disabled', !isDers);

        // Üniversite ve bölüm seçim alanlarının görünürlüğü
        $("#university-department-select").toggle(isDers);
    }).trigger('change'); // Sayfa yüklendiğinde değişiklik tetiklenir
});
