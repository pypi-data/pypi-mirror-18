

########################################################################
class SliderH

    #----------------------------------------------------------------------
    constructor: (sliderh, parent) ->

        threshold = $(parent).data("threshold")
        if not threshold
            threshold = 0.25

        @DIRTY = false
        @WIDTH_SLIDER = $(sliderh).width()
        @WIDTH_SLIDER_THRESHOLD = @WIDTH_SLIDER * threshold
        @WIDTH_MAX_SLIDER = $(parent).width() - @WIDTH_SLIDER



    #----------------------------------------------------------------------
    get_parent: (event) =>
        cls = @
        parent = $(event.srcEvent.path[1])


        if not parent.hasClass("d4a-sliderh-parent")
            parent = parent.parents(".d4a-sliderh-parent")

        #if not parent.hasClass("d4a-sliderh-parent")
            #parent = parent.parent(".d4a-sliderh-parent")

        #if not parent.hasClass("d4a-sliderh-parent")
            #parent = parent.parent(".d4a-sliderh-parent")

        #if not parent.hasClass("d4a-sliderh-parent")
            #parent = parent.parent(".d4a-sliderh-parent")

        #console.log(parent)

        return parent


    #----------------------------------------------------------------------
    start_pand_single: (event) =>
        cls = @

        parent = cls.get_parent(event)


        cls.OFFSET = parseInt(parent.css("transform").split(',')[4])

        for s in [1..11]
            if cls.OFFSET < @WIDTH_SLIDER*s
                cls.OFFSET = @WIDTH_SLIDER*s
                break

        if not cls.OFFSET
            cls.OFFSET = 0

        if cls.OFFSET > 0
            cls.OFFSET = 0

        cls.DIRTY = true


    #----------------------------------------------------------------------
    start_pand_end: (event) =>
        cls = @
        #parent = $(event.srcEvent.path[1])
        #console.log(parent
        parent = cls.get_parent(event)

        if cls.DIRTY
            parent.css({"-webkit-transition-duration": "0.2s"})
            parent.css({"-webkit-transform": "translateX(#{cls.OFFSET}px)"})

        else
            fn=()->
                if cls.OFFSET
                    console.log("Running: "+parent.data("onmove"))
                    eval(parent.data("onmove"))
                else
                    console.log("Fake")
            setTimeout(fn, 200)


    #----------------------------------------------------------------------
    start_pand: (event) =>
        cls = @
        #parent = $(event.srcEvent.path[1])
        parent = cls.get_parent(event)

        X = cls.OFFSET + event.deltaX

        if cls.OFFSET is 0 and event.deltaX > 0
            return

        if cls.OFFSET is -cls.WIDTH_MAX_SLIDER and event.deltaX < 0
            return

        parent.css({"-webkit-transition-duration": "0s"})
        parent.css({"-webkit-transform": "translateX(#{X}px)"})

        if event.deltaX < -cls.WIDTH_SLIDER_THRESHOLD
            W = cls.OFFSET - cls.WIDTH_SLIDER
            parent.css({"-webkit-transition-duration": "0.2s"})
            parent.css({"-webkit-transform": "translateX(#{W}px)"})
            cls.DIRTY = false


            fn=()->
                eval(parent.data("onmove"))
            setTimeout(fn, 200)

            return

        if event.deltaX > cls.WIDTH_SLIDER_THRESHOLD
            W = cls.OFFSET + cls.WIDTH_SLIDER
            parent.css({"-webkit-transition-duration": "0.2s"})
            parent.css({"-webkit-transform": "translateX(#{W}px)"})
            cls.DIRTY = false
            return


$(document).ready ->





#Contructor
#----------------------------------------------------------------------


    window.initsliders=()->

        for element in $(".d4a-sliderh-parent")
            SliderH_ = new SliderH($(element).children(".d4a-sliderh"), element)
            ASH_slider = new Hammer(element)
            ASH_slider.get("pan").set({velocity: 0, pointers: 1, threshold: 0})


            ASH_slider.on "panleft panright", SliderH_.start_pand
            ASH_slider.on "panstart", SliderH_.start_pand_single
            ASH_slider.on "panend", SliderH_.start_pand_end


    window.initsliders()

