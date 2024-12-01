$(function () {
    $("#id_kategori").change(function () {
        const isDers = $(this).val() === "ders";
        $("#id_ders_kategori").closest(".mb-3").toggle(isDers);
        $("#id_ders_kategori").prop('disabled', !isDers);
        $(".form-check.mb-3").toggle(isDers);
        $("#id_is_shared").prop('disabled', !isDers);
    }).trigger('change');
});
