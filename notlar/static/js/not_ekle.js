$(function () {
    $("#id_kategori, #id_is_shared").change(function () {
        const isDers = $("#id_kategori").val() === "ders";
        const isShared = $("#id_is_shared").prop('checked');
        if (isDers && isShared) {
            $("#id_file").prop('required', true);  
        } else {
            $("#id_file").prop('required', false); 
        }
        $("#id_ders_kategori").closest(".mb-3").toggle(isDers);
        $("#id_ders_kategori").prop('disabled', !isDers);
        $(".form-check.mb-3").toggle(isDers);
        $("#id_is_shared").prop('disabled', !isDers);
    }).trigger('change');
});
