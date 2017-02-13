(function($){
  
  var $project = $('#project');

  var projects = [
    {
      value: "1",
      label: "Tea-coffe",
      desc: "the write less, do more, JavaScript library",
      icon: "tea.png"
    },
    {
      value: "2",
      label: "Bajji",
      desc: "the official user interface library for jQuery",
      icon: "bajji.png"
    },
    {
      value: "3",
      label: "Bun",
      desc: "a pure-JavaScript CSS selector engine",
      icon: "bun.png"
    },{
      value: "4",
      label: "Chakuli",
      desc: "the write less, do more, JavaScript library",
      icon: "chakuli.png"
    },
    {
      value: "5",
      label: "Biscuit",
      desc: "the official user interface library for jQuery",
      icon: "biscuit.png"
    },
    {
      value: "6",
      label: "Chocolate",
      desc: "a pure-JavaScript CSS selector engine",
      icon: "chocolate.png"
    }
,
    {
      value: "7",
      label: "Dry-Fruits",
      desc: "a pure-JavaScript CSS selector engine",
      icon: "dryfruits.png"
    }
,
    {
      value: "8",
      label: "Juice",
      desc: "a pure-JavaScript CSS selector engine",
      icon: "juice.png"
    }
,
    {
      value: "9",
      label: "Tissu",
      desc: "a pure-JavaScript CSS selector engine",
      icon: "tiss.png"
    }
,
    {
      value: "10",
      label: "Water-can",
      desc: "a pure-JavaScript CSS selector engine",
      icon: "water-can.png"
    }

  ];
  
  $project.autocomplete({
    minLength: 0,
    source: projects,
    focus: function( event, ui ) {
      $project.val( ui.item.label );
      return false;
    }
  });
  
  $project.data( "ui-autocomplete" )._renderItem = function( ul, item ) {
    
    var $li = $('<li>'),
        $img = $('<img>');


    $img.attr({
      src: 'item_pics/' + item.icon,
      alt: item.label
    });

    $li.attr('data-value', item.label);
    $li.append('<a href="#">');
    $li.find('a').append($img).append(" " + item.label);    

    return $li.appendTo(ul);
  };
  

})(jQuery);
