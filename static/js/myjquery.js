/**
 * Created by Maria on 06/12/2016.
 */


function updateCheckboxes(){

     $('input:checkbox').addClass("bt-switch").attr({
        'data-on-text': "Yes",
        'data-off-text': "No",
        'data-on-color': "info",
        'data-off-color': "danger"
    });

    $(".bt-switch").bootstrapSwitch();


}

function updateDateFields_showToday(){

    $('#id_start_date').addClass("sm-form-control").addClass("tleft").addClass("default").attr({
        'placeholder': "MM/DD/YYYY"
    });

    $('#id_end_date').addClass("sm-form-control").addClass("tleft").addClass("default").attr({
        'placeholder': "MM/DD/YYYY"
    });

    $('#id_end_date').css("width","100%").css("box-sizing","border-box").css("border", "none");
    $('#id_start_date').css("width","100%").css("box-sizing","border-box").css("border", "none");

}

function dropdown_check(){

    $(document).ready(function(){
    $('.dropdown').on('show.bs.dropdown', function(){
        alert('The dropdown is about to be shown.');
    });
    $('.dropdown').on('shown.bs.dropdown', function(){
        alert('The dropdown is now fully shown.');
    });
    $('.dropdown').on('hide.bs.dropdown', function(e){
        alert('The dropdown is about to be hidden.');
    });
    $('.dropdown').on('hidden.bs.dropdown', function(){
        alert('The dropdown is now fully hidden.');
    });
});
}

$(function() {
    $('.travel-date-group .default').datepicker({
        autoclose: true,
        startDate: "today",
    });

    $('.travel-date-group .today').datepicker({
        autoclose: true,
        startDate: "today",
        todayHighlight: true
    });

    $('.travel-date-group .past-enabled').datepicker({
        autoclose: true,
    });
    $('.travel-date-group .format').datepicker({
        autoclose: true,
        format: "dd-mm-yyyy",
    });

    $('.travel-date-group .autoclose').datepicker();

    $('.travel-date-group .disabled-week').datepicker({
        autoclose: true,
        daysOfWeekDisabled: "0"
    });

    $('.travel-date-group .highlighted-week').datepicker({
        autoclose: true,
        daysOfWeekHighlighted: "0"
    });

    $('.travel-date-group .mnth').datepicker({
        autoclose: true,
        minViewMode: 1,
        format: "mm/yy"
    });

    $('.travel-date-group .multidate').datepicker({
        multidate: true,
        multidateSeparator: " , "
    });

    $('.travel-date-group .input-daterange').datepicker({
        autoclose: true
    });

    $('.travel-date-group .inline-calendar').datepicker();

    $('.datetimepicker').datetimepicker({
        showClose: true
    });

    $('.datetimepicker1').datetimepicker({
        format: 'LT',
        showClose: true
    });

    $('.datetimepicker2').datetimepicker({
        inline: true,
        sideBySide: true
    });

});

$(function() {
    // .daterange1
    $(".daterange1").daterangepicker({
        "buttonClasses": "button button-rounded button-mini nomargin",
        "applyClass": "button-color",
        "cancelClass": "button-light"
    });

    // .daterange2
    $(".daterange2").daterangepicker({
        "opens": "center",
        timePicker: true,
        timePickerIncrement: 30,
        locale: {
            format: 'MM/DD/YYYY h:mm A'
        },
        "buttonClasses": "button button-rounded button-mini nomargin",
        "applyClass": "button-color",
        "cancelClass": "button-light"
    });

    // .daterange3
    $(".daterange3").daterangepicker({
        singleDatePicker: true,
        showDropdowns: true
    },
    function(start, end, label) {
        var years = moment().diff(start, 'years');
        alert("You are " + years + " years old.");
    });

    // reportrange
    function cb(start, end) {
        $(".reportrange span").html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
    }
    cb(moment().subtract(29, 'days'), moment());

    $(".reportrange").daterangepicker({
        "buttonClasses": "button button-rounded button-mini nomargin",
        "applyClass": "button-color",
        "cancelClass": "button-light",
        ranges: {
           'Today': [moment(), moment()],
           'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
           'Last 7 Days': [moment().subtract(6, 'days'), moment()],
           'Last 30 Days': [moment().subtract(29, 'days'), moment()],
           'This Month': [moment().startOf('month'), moment().endOf('month')],
           'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
        }
    }, cb);

    // .daterange4
    $(".daterange4").daterangepicker({
        autoUpdateInput: false,
        locale: {
            cancelLabel: 'Clear'
        },
        "buttonClasses": "button button-rounded button-mini nomargin",
        "applyClass": "button-color",
        "cancelClass": "button-light"
    });

    $(".daterange4").on('apply.daterangepicker', function(ev, picker) {
        $(this).val(picker.startDate.format('MM/DD/YYYY') + ' - ' + picker.endDate.format('MM/DD/YYYY'));
    });

    $(".daterange4").on('cancel.daterangepicker', function(ev, picker) {
        $(this).val('');
    });

});


