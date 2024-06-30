/* Dashboard */

    $(document).ready(function() {
        $('.likeButton').click(function() {
            var post_id = $(this).data('post-id');
            var button = $(this);
            $.ajax({
                type: 'POST',
                url: '/like/',
                data: {
                    'post_id': post_id,
                    'csrfmiddlewaretoken': '{{ csrf_token }}'
                },
                dataType: 'json',
                success: function(response) {
                    if (response.liked) {
                        $('#likeText', button).text('Liked');
                    } else {
                        $('#likeText', button).text('Like');
                    }
                    $('#likeCount', button).text(response.like_count);
                },
                error: function(response) {
                    console.log('Error:', response);
                }
            });
        });
    });


/* Messages */

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $(document).ready(function() {
        $('#message-form').on('submit', function(e) {
            e.preventDefault();
            var form = $(this);
            $.ajax({
                type: 'POST',
                url: form.attr('action'),
                data: form.serialize(),
                success: function(response) {
                    if (response.success) {
                        var newMessage = '<div class="message ' + (response.sender == '{{ user.username }}' ? 'sent' : 'received') + '">' +
                                            '<strong>' + response.sender_name + ':</strong> ' +
                                            '<p>' + response.message + '</p>' +
                                            '<span class="timestamp">' + response.timestamp + '</span>' +
                                        '</div>';
                        
                        $('#conversation').append(newMessage);
                        
                        var conversation = $('#conversation');
                        conversation.scrollTop(conversation[0].scrollHeight);
                        
                        $('#content').val('');
                    }
                }
            });
        });
    });
    
/* Profile */

    $(document).ready(function() {
        $('.custom-file-input').on('change', function(event) {
            var inputFile = event.currentTarget;
            $(inputFile).parent().find('.custom-file-label').html(inputFile.files[0].name);
        });
    });

