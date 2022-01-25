

window.onload = function ()
{
    function loadMeters()
    {
        table = $('#table_meters').DataTable({
            "serverSide": true,
            "processing": true,
            "ajax": function (data, callback, settings)
            {
                var sort_column_name = data.columns[data.order[0].column].data.replace(/\./g, "__");
                var direction = "";
                if (data.order[0].dir == "desc") { direction = "-" };
                $.get(meterlUrl, {
                    limit: data.length,
                    start: data.start,
                    filter: data.search.value,
                    order_by: direction + sort_column_name
                }, function (res)
                {
                    callback({
                        recordsTotal: res.length,
                        recordsFiltered: res.length,
                        data: res.objects
                    });
                });
            },
            columns: [
                {
                    "data": "id", "render": function (data, type, row)
                    {
                        return '<td class="selected"><input type="checkbox" id="item_20" value="20"><label for="item_20"><span></span></label></td>'
                    }
                },
                {
                    "data": "id", "render": function (data, type, row)
                    {
                        if ('{{ request.user.is_superuser }}' == 'True')
                        {
                            return '<center>' +
                                '<div class="btn-group">' +
                                '<a href="#" class="btn btn-warning btn-xs text-sm" title="Edit" onclick = "" ><i class="fas fa-pencil-alt"></i><span style="font-size: 12px;"> Edit</span></a>' +
                                '</div>' +
                                '</center>'
                        }
                        else
                        {
                            return '<center>' +
                                '<div class="btn-group">' +
                                '<a href="" class="btn btn-warning btn-xs text-sm" title="Edit"><i class="fal fa-pencil-alt"></i><span style="font-size: 12px;"> Edit</span></a>' +
                                '</div>' +
                                '</center>'
                        }
                    }
                },
                // {
                //     "data": "acquisitionid__transactiondate", "render": function (data, type, row)
                //     {
                //         return '<td style="width: fit-content;"> <a href="">' + data + '</a></td>'
                //     }
                // },
                { "data": "acquisitionid__transactiondate" },
                { "data": "brandid__brand" },
                { "data": "ampheres" },
                { "data": "mtypeid__metertype" },
                { "data": "units" },

            ],
            // "scrollX": true,
            "searching": false,
            "info": false,
            "paging": true,
            "autoWidth": true,
            "responsive": true,
            "columnDefs": [
                // { "targets": [0], "searchable": false, "orderable": false,},
                { "targets": [0, 1], "searchable": false, "orderable": false, "visible": false, "width": "54%" },
                { "targets": [6], "className": "text-right" }
            ],
            "keys": true,
            "keys": { "blurable": false },
            "select": true,
            "select": {
                "style": 'single',
                "selector": 'td:first-child',
            },
            "dom": '<"top"i>rt<"bottom"flp><"clear">',
            "fnInitComplete": function (oSettings, json)
            {
                $('#table_meters').css('width', '100%');
                $("#table_meters").wrap("<div style='overflow:auto; width:100%;position:relative;'></div>");
                $('#table_meters tbody tr:eq(0)').click();
            },
        });
    }
    loadMeters();

    $('#table_meters tbody').on('click', 'tr', function ()
    {
        if ($(this).hasClass('selected'))
        {
            $(this).removeClass('selected');
        }
        else
        {
            table.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
        }

        var data = table.rows(this).data();
        var id = data[0]['id'];
        selectedmeterid = id;
        $("#table_meterdetails").dataTable().fnDestroy();
        loadDetails(id);
        // $('#table_meterdetails').DataTable().ajax.reload(null, false);
    });

    $(window).bind('resize', function ()
    {
        $("#table_meters").wrap("<div style='overflow:auto; width:100%;position:relative;'></div>");
        $("#table_meterdetails").wrap("<div style='overflow:auto; width:100%;position:relative;'></div>");
        $('#table_meters').css('width', '100%');
        $('#table_meterdetails').css('width', '100%');
    });

    jQuery('.table_meters').wrap('<div class="dataTables_scroll" />');
    jQuery('.table_meterdetails').wrap('<div class="dataTables_scroll" />');

    $('#select_all').on('click', function ()
    {
        var rows = table.rows({ 'search': 'applied' }).nodes();
        $('input[type="checkbox"]', rows).prop('checked', this.checked);
    });

    function loadDetails(id)
    {
        let stats = [ 'For calibration', 'Pass', 'Failed' ];
        tabledetails = $('#table_meterdetails').DataTable({
            "serverSide": true,
            "processing": true,
            "ajax": function (data, callback, settings)
            {
                var sort_column_name = data.columns[data.order[0].column].data.replace(/\./g, "__");
                var direction = "";
                if (data.order[0].dir == "desc") { direction = "-" };
                $.get(mDetailsUrl, {
                    id: id,
                    limit: data.length,
                    start: data.start,
                    filter: data.search.value,
                    order_by: direction + sort_column_name
                }, function (res)
                {
                    callback({
                        recordsTotal: res.length,
                        recordsFiltered: res.length,
                        data: res.objects
                    });
                });
            },
            columns: [
                {
                    "data": "id", "render": function (data, type, row)
                    {
                        return '<td class="selected"><input type="checkbox" id="item_20" value="20"><label for="item_20"><span></span></label></td>'
                    }
                },
                {
                    "data": "id", "render": function (data, type, row)
                    {
                        if (row["status"] > 0)
                        {
                            return '<center>' +
                                '<div class="btn-group">' +
                                '<a href="#" class="btn btn-default btn-xs text-sm" title="Calibrated" onclick=""><span style="font-size: 12px;"> Calibrated</span></a>' +
                                '</div>' +
                                '</center>'
                        }
                        else
                        {
                            return '<center>' +
                                '<div class="btn-group">' +
                                '<a href="single/' + row["id"] + '" class="btn btn-info btn-xs text-sm" title="Calibrate" onclick=""><span style="font-size: 12px;"> Calibrate</span></a>' +
                                '</div>' +
                                '</center>'
                            }
                    }
                },
                { "data": "serialno" },
                { "data": "accuracy" },
                {
                    "data": "status", "render": function (data, type, row)
                    {
                        return '<span style="font-size: 12px;"> ' + stats[row["status"]] +'</span>'
                    }
                },

            ],
            // "scrollX": true,
            "searching": false,
            "info": false,
            "paging": true,
            "autoWidth": true,
            "responsive": true,
            "columnDefs": [
                { "targets": [0], "searchable": false, "orderable": false, "visible": false },
                // { "targets": [0], "searchable": false, "orderable": false,},
                { "targets": [1], "width": "14%" },
            ],
            "keys": true,
            "keys": { "blurable": false },
            "select": true,
            "select": {
                "style": 'multi',
                "selector": 'td:first-child',
            },
            "dom": '<"top"i>rt<"bottom"flp><"clear">',
            "fnInitComplete": function (oSettings, json)
            {
                $('#table_meterdetails').css('width', '100%');
                $("#table_meterdetails").wrap("<div style='overflow:auto; width:100%;position:relative;'></div>");
            //     $('#table_meterdetails tbody tr:eq(0)').click();
            },
        });
    }


}
function loadMultiple(params)
{
    window.open(mMultiUrl.replace('0', selectedmeterid), "_self");
}

// function return_selectedTable() {
//     var itemcode, qty;
//     var count = table.rows('.selected').count();
//     if (count <= 0) return;
//     var ok = confirm('Are you sure to return selected row(s) to warehouse?');
//     if (ok == true) {
//         data = table.rows('.selected').data();
//         data.each(function (value, index) {
//             if (value['status'] == "None" || value['status'] == null ) {
//                 alert('Meter ' + value['serialno'] + " is not yet calibrated!")
//             } else {
//                 save_return_selectedTable(value['id'], value['serialno']);
//             }
//         });
//     }
// }

// function save_return_selectedTable(id=0, serialno='') {
//     $.ajax({
//         url: "",
//         method: 'GET',
//         type: 'GET',
//         data: { id: id, },
//         success: function (data) {
//              $.ajax({
//                 success: function (data) {
//                     table.ajax.reload(null, false);
//                     msgalert("Returned", "Meter ["+ serialno +"] successfully returned to warehouse", 1);
//                 },
//                 error: function () {
//                     alert('Err: save_return_selectedTable');
//                 }
//             });
//         },
//     });
// }