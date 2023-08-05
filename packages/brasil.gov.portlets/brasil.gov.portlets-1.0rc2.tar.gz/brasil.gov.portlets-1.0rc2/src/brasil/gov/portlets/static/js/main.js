var root = typeof exports !== "undefined" && exports !== null ? exports : this;

$(function() {
    portletsManager.init();
    portlets.init();
});

var portletsManager = {
    init: function() {
        this.collection();
        this.audiogallery();
        this.video();
        this.videogallery();
        this.mediacarousel();
    },
    collection: function() {
        if ($('h1.documentFirstHeading').text().indexOf('Portal Padrão Coleção') > 0) {
            var update_image = function() {
                if ($('#form\\.show_image').is(':checked')) {
                    $('#formfield-form-image_size').show();
                } else {
                    $('#formfield-form-image_size').hide();
                }
            };
            var update_footer = function() {
                if ($('#form\\.show_footer').is(':checked')) {
                    $('#formfield-form-footer').show();
                    $('#formfield-form-footer_url').show();
                } else {
                    $('#formfield-form-footer').hide();
                    $('#formfield-form-footer_url').hide();
                }
            };
            var update_date = function() {
                if ($('#form\\.show_date').is(':checked')) {
                    $('#formfield-form-show_time').show();
                } else {
                    $('#formfield-form-show_time').hide();
                }
            }
            var insert_collection_warning = function() {
                var html = '<div>' +
                           '    <span class="warning">' +
                           '        ATENÇÃO: Para coleções de Evento ou Compromisso (Agenda), será utilizada a data do Evento/Compromisso para ordenação e exibição, e não a data informada na coleção.' +
                           '     </span>' +
                           '</div>';
                $('#formfield-form-collection fieldset').append(html);
            }
            $('#form\\.show_image').on('click', update_image);
            $('#form\\.show_footer').on('click', update_footer);
            $('#form\\.show_date').on('click', update_date);
            update_image();
            update_footer();
            update_date();
            insert_collection_warning();
        }
    },
    audiogallery: function() {
        if ($('h1.documentFirstHeading').text().indexOf('Portal Padrão Galeria de Áudios') > 0) {
            var update_title = function() {
                if ($('#form\\.show_header').is(':checked')) {
                    $('#formfield-form-header').show();
                    $('#formfield-form-header_type').show();
                } else {
                    $('#formfield-form-header').hide();
                    $('#formfield-form-header_type').hide();
                }
            };
            var update_footer = function() {
                if ($('#form\\.show_footer').is(':checked')) {
                    $('#formfield-form-footer').show();
                    $('#formfield-form-footer_url').show();
                } else {
                    $('#formfield-form-footer').hide();
                    $('#formfield-form-footer_url').hide();
                }
            };
            $('#form\\.show_header').on('click', update_title);
            $('#form\\.show_footer').on('click', update_footer);
            update_title();
            update_footer();
        }
    },
    video: function() {
        if ($('h1.documentFirstHeading').text().indexOf('Portal Padrão Vídeo') > 0) {
            var update_title = function() {
                if ($('#form\\.show_header').is(':checked')) {
                    $('#formfield-form-header').show();
                } else {
                    $('#formfield-form-header').hide();
                }
            };
            $('#form\\.show_header').on('click', update_title);
            update_title();
        }
    },
    videogallery: function() {
        if ($('h1.documentFirstHeading').text().indexOf('Portal Padrão Galeria de Vídeos') > 0) {
            var update_header = function() {
                if ($('#form\\.show_header').is(':checked')) {
                    $('#formfield-form-header').show();
                    $('#formfield-form-header_type').show();
                } else {
                    $('#formfield-form-header').hide();
                    $('#formfield-form-header_type').hide();
                }
            };
            var update_footer = function() {
                if ($('#form\\.show_footer').is(':checked')) {
                    $('#formfield-form-footer').show();
                    $('#formfield-form-footer_url').show();
                } else {
                    $('#formfield-form-footer').hide();
                    $('#formfield-form-footer_url').hide();
                }
            };
            $('#form\\.show_header').on('click', update_header);
            $('#form\\.show_footer').on('click', update_footer);
            update_header();
            update_footer();
        }
    },
    mediacarousel: function() {
        if ($('h1.documentFirstHeading').text().indexOf('Portal Padrão Carrossel de Imagens') > 0) {
            var update_header = function() {
                if ($('#form\\.show_header').is(':checked')) {
                    $('#formfield-form-header').show();
                    $('#formfield-form-header_type').show();
                } else {
                    $('#formfield-form-header').hide();
                    $('#formfield-form-header_type').hide();
                }
            };
            var update_footer = function() {
                if ($('#form\\.show_footer').is(':checked')) {
                    $('#formfield-form-footer').show();
                    $('#formfield-form-footer_url').show();
                } else {
                    $('#formfield-form-footer').hide();
                    $('#formfield-form-footer_url').hide();
                }
            };
            $('#form\\.show_header').on('click', update_header);
            $('#form\\.show_footer').on('click', update_footer);
            update_header();
            update_footer();
        }
    },
};

var portlets = {
    init: function() {
        this.audio();
        this.audiogallery();
        this.videogallery();
        this.mediacarousel();
        this.cycle2();
    },
    audio: function() {
        if (!$.fn.audio_player) {
            function AudioPlayer(audio_element, conf) {
                var self = this,
                    cssSelectorAncestor = conf.cssSelectorAncestor,
                    ae = audio_element;

                $.extend(self, {
                    init: function(){
                        var audio_url = self.get_audio_url();
                        var media = self.get_media(audio_url);

                        ae.jPlayer({
                            ready: function () {
                                $(this).jPlayer("setMedia", media.media_urls);
                            },
                            swfPath: "/++resource++brasil.gov.portlets/js",
                            supplied: media.supplied,
                            cssSelectorAncestor: cssSelectorAncestor,
                            solution:"html,flash",
                            wmode: "window",
                            preload: "none"
                        });
                    },

                    /**
                     * Construct the setMedia list of option and the supplied list
                     **/
                    get_media: function(urls){
                        var media = {'media_urls':{}, 'supplied':''};
                        var media_type, url, _i, _len;

                        urls = urls.split(';');
                        for (_i = 0, _len = urls.length; _i < _len; _i++) {
                            url = urls[_i];
                            media_type = self.get_media_type(url);
                            if (media_type){
                                media['media_urls'][media_type] = url;
                                if (media['supplied']) {
                                    media['supplied'] += ', ';
                                }
                                media['supplied'] += media_type;

                            }
                        }

                        return media;
                    },

                    /**
                     * Get the audio url from the configuration or the data attribute in the
                     * main element
                     **/
                    get_audio_url: function(){
                        var url = conf.audio_url? conf.audio_url : ae.data('audio-url');
                        return url;
                    },

                    /**
                     * Function to gleam the media type from the URL
                     *
                     **/
                    get_media_type: function(url) {
                        var mediaType = false;
                        if(/\.mp3$/i.test(url)) {
                            mediaType = 'mp3';
                        } else if(/\.mp4$/i.test(url) || /\.m4v$/i.test(url)) {
                            mediaType = 'm4v';
                        } else if(/\.m4a$/i.test(url)) {
                            mediaType = 'm4a';
                        } else if(/\.ogg$/i.test(url) || /\.oga$/i.test(url)) {
                            mediaType = 'oga';
                        } else if(/\.ogv$/i.test(url)) {
                            mediaType = 'ogv';
                        } else if(/\.webm$/i.test(url)) {
                            mediaType = 'webmv';
                        }
                        return mediaType;
                    },

                    /**
                     * Method to update the media element reproduced in the player
                     * requires just a media url
                     **/
                    update_player: function(new_url) {
                        //clear all media (even if is running)
                        //ae.jPlayer("clearMedia");
                        conf.audio_url = new_url;

                        var audio_url = self.get_audio_url();
                        var media = self.get_media(audio_url);

                        ae.jPlayer( "clearMedia" );
                        ae.jPlayer("option", 'swfPath', '/++resource++brasil.gov.portlets/js');

                        ae.jPlayer("option", "supplied", media.supplied);
                        ae.jPlayer("setMedia", media.media_urls);

                    }
                });
                self.init();
            }

            $.fn.audio_player = function(options) {

                // already instanced, return the data object
                var el = this.data("audio_player");
                if (el) { return el; }


                var default_settings = this.data('audio_player-settings');
                var settings = '';
                //default settings
                if (default_settings) {
                    settings = default_settings;
                } else {
                    settings = {
                        'cssSelectorAncestor': '#jp_container_1',
                    }
                }

                if (options) {
                    $.extend(settings, options);
                }

                return this.each(function() {
                    el = new AudioPlayer($(this), settings);
                    $(this).data("audio_player", el);
                });

            };
        }
        $('.portal-padrao-audio-portlet').each(function(){
            var playerid = $('#'+this.id+' .jp-jplayer')[0].id;
            var containerid = $('#'+this.id+' .jp-audio')[0].id;
            $('#'+playerid).audio_player({'cssSelectorAncestor':'#'+containerid});
        });
    },
    audiogallery: function() {
        if (!$.fn.audiogallery) {
            function AudioGallery(gallery) {
                var self = this,
                    gallery_obj = gallery,
                    player = gallery_obj.find('.jp-jplayer'),
                    ancestor = '#' + gallery_obj.find('.jp-audio').attr('id');

                $.extend(self, {
                    init: function(){
                        self.bind_events();
                        player.audio_player({'cssSelectorAncestor':ancestor});
                    },

                    bind_events: function() {
                        var links = gallery_obj.find('.audiogallery-item');
                        links.click(function(e){
                            e.preventDefault();
                            self.update($(this).attr('href'));
                            links.parent('li').removeClass('selected');
                            $(this).parent('li').addClass('selected');
                            gallery_obj.find('.audiogallery-item-title').html($(this).html());
                        });
                    },

                    update: function(url) {
                        var p = player.audio_player({'cssSelectorAncestor':ancestor});
                        p.update_player(url);
                    }
                });
                self.init();
            }

            $.fn.audiogallery = function() {

                // already instanced, return the data object
                var el = this.data("audiogallery");
                if (el) { return el; }


                var default_settings = this.data('audiogallery-settings');

                return this.each(function() {
                    el = new AudioGallery($(this));
                    $(this).data("audiogallery", el);
                });

            };
        }
        $('.portal-padrao-audiogallery-portlet').each(function(){
            $('#'+this.id).audiogallery();
        });
    },
    videogallery: function() {
        var fix_player_size = function() {
            $('.portal-padrao-videogallery-portlet').each(function(){
                var $portlet = $(this);
                $('.portlet-videogallery-player', $portlet).each(function() {
                    var $container = $(this);
                    var $player = $('iframe', $container);
                    var width = parseInt($container.width()) - (parseInt($container.css('padding-left')) * 2);
                    var height = parseInt(width * 10 / 16);
                    $player.width(width);
                    $player.height(height);
                });
            });
        };
        $(window).resize(fix_player_size);
        fix_player_size();
    },
    mediacarousel: function() {
        var fix_player_size = function() {
            $('.portal-padrao-mediacarousel-portlet').each(function(){
                var $portlet = $(this);
                $('.portlet-mediacarousel-player', $portlet).each(function() {
                    var $container = $(this);
                    var $player = $('img', $container);
                    var width = $container.width();
                    var height = parseInt(width * 10 / 16);
                    $player.css('max-height', height);
                });
            });
        };
        $(window).resize(fix_player_size);
        fix_player_size();
    },
    cycle2: function() {
        if (!root.cycle2_loaded) {
            root.cycle2_loaded = true;

            var obj = this;
            $('.cycle-slideshow').on('cycle-next cycle-prev', function (e, opts) {
                var $galeria = $(this).parent().parent();
                var $slideshows = $('.cycle-slideshow', $galeria);
                $slideshows.not(this).cycle('goto', opts.currSlide);
                obj.layoutAdjustment($galeria, opts.currSlide);
            });

            // Aplicando o mesmo controle de navegacao para os thumbs e galerias
            $('.cycle-carrossel .thumb-itens').click(function (e){
                e.preventDefault();
                var $thumbs = $(this).parent().parent();
                var $galeria = $thumbs.parent().parent();
                var $slideshows = $('.cycle-slideshow', $galeria);
                var index = $thumbs.data('cycle.API').getSlideIndex(this);
                $slideshows.cycle('goto', index);
                obj.layoutAdjustment($galeria, index);
            });

            $('.cycle-pager .thumb-itens').click(function (e){
                e.preventDefault();
                var $thumbs = $(this).parent().parent();
                var $galeria = $thumbs.parent().parent();
                var $slideshows = $('.cycle-slideshow', $galeria);
                var index = parseInt($(this).data('slide-index'));
                $slideshows.cycle('goto', index);
                obj.layoutAdjustment($galeria, index);
            });

            // Adicionando navegação por teclado
            $(document.documentElement).keyup(function (event) {
                if (event.keyCode == 37) {
                    $('.cycle-prev').trigger('click');
                } else if (event.keyCode == 39) {
                    $('.cycle-next').trigger('click');
                }
            });

            $('.cycle-slideshow').each(function(){
                var $galeria = $(this).parent().parent();
                obj.layoutAdjustment($galeria, 0);
            });
        }
    },
    layoutAdjustment: function($galeria, index){
        var aElem = $(".cycle-player .cycle-slide", $galeria),
        elem,
        novaaltura,
        alturaimagem,
        larguracarosel;

        // Pula primeiro elemento
        index = index + 1;
        elem = aElem[index],
        novaaltura = $(elem).height();
        alturaimagem = $('.cycle-sentinel img', $galeria).height();
        if ($('.carousel', $galeria).length != 0) {
            larguracarosel = ($('.carousel', $galeria).width() -
                              (36 * 2));
        }
        if ($('.portlet-mediacarousel-carousel', $galeria).length != 0) {
            larguracarosel = ($('.portlet-mediacarousel-carousel', $galeria).width() -
                              (32 * 2));
        }

        $('.cycle-sentinel', $galeria).height(novaaltura);
        $('.cycle-hover', $galeria).height(alturaimagem);
        $('.cycle-carrossel', $galeria).width(larguracarosel);
    },
};

