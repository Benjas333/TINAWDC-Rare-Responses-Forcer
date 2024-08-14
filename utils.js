const auto_open_urls = true;
const code_element = document.querySelector('.code');
const code = code_element.getAttribute('data-value');

window.onload = () => {
        var link_elements = document.querySelectorAll('.has-link');
        
        link_elements.forEach((element) => {
                element.className += ' flex flex-col gap-y-8 text-white'
                var links = element.getAttribute('data-links');
                if (!links) {
                        return;
                }
                var urls = links.split(';');
                urls.forEach((url) => {
                        var message_div = document.createElement('div');
                        message_div.className = 'relative text-2xl md:text-4xl except-mobile font-kidwriting';
                
                        if (url.startsWith('http')) {
                                message_div.innerHTML = `Link redirection detected: ${url}`;
                                var button = document.createElement('button');
                                button.className = 'content-button';
                                button.innerHTML = '<small>➔</small> OPEN LINK';
                                button.onclick = () => {
                                        window.open(url.trim(), '_blank');
                                };
                                message_div.appendChild(button);
                                if (auto_open_urls) window.open(url.trim(), '_blank');
                        } else {
                                var targetElement = document.getElementById(url.trim());
                                message_div.innerHTML = targetElement ? `Here should be rendered the '${url.trim()}' element.` : `Invalid ID or link: ${url.trim()}`;
                        }
                        element.appendChild(message_div);
                });
        });

        var text_elements = document.querySelectorAll('.has-text');
        
        text_elements.forEach((element) => {
                var text = element.getAttribute('data-text');
                element.innerHTML = `<div id="desk_frame" class="part-of-ui relative flex items-center justify-center w-[200vw] sm:w-screen sm:min-h-dvh overflow-hidden text-white/90 print:hidden" data-controller="secrets" data-secrets-loaded1-value="true" data-secrets-loaded2-value="true" data-secrets-ready-value="true" data-secrets-waiting-value="true" data-secrets-bgm-playing-value="rain" data-secrets-begun-value="true" data-secrets-screen-occupied-value="true" data-secrets-screen-loops-value="0" data-secrets-video-playing-value="" data-secrets-static-playing-value="static2"><div id="desk_form" class="part-of-ui container relative items-center justify-center aspect-video max-w-6xl" autocomplete="off" spellcheck="false" data-action="secrets#submit:prevent"><div id="screen_overlay" class="part-of-ui absolute top-0 right-0 left-0 bottom-0 opacity-0 pointer-events-none z-30 scale-[1.015] brightness-[1.35] saturate-[1.35] transition-all duration-150 !opacity-100" data-secrets-target="screenOverlay"><img src="https://www.thisisnotawebsitedotcom.com/assets/screen-overlay.png" aria-hidden="true"></div><video id="screen_static" class="part-of-ui absolute w-[20.5%] top-[14%] left-[22.25%] object-cover z-20 transition-all duration-150 opacity-0 aspect-square !opacity-100" aria-hidden="true" playsinline="" loop="" autoplay="" preload="auto" disablepictureinpicture="" data-secrets-target="screenStatic"><source src="https://www.thisisnotawebsitedotcom.com/assets/static-3.mp4" type="video/mp4"></video><div id="screen_text" class="part-of-ui absolute flex items-center justify-center w-[20.5%] top-[14%] left-[22.25%] aspect-square text-center px-4 bg-black/90 opacity-0 transition-opacity duration-150 z-20 text-white text-glow font-mono text-xs leading-tight sm:text-sm md:text-base overflow-hidden !opacity-100" data-secrets-target="screenText">${text}</div><video id="desk1" class="part-of-ui absolute top-0 right-0 left-0 bottom-0 object-contain pointer-events-none scale-[1.014]" alt="A desk..." aria-hidden="true" muted="" playsinline="" loop="" autoplay="" preload="auto" data-secrets-target="video1" data-action="loadeddata->secrets#loaded1 ended->secrets#videoLoop"><source src="https://www.thisisnotawebsitedotcom.com/assets/bg-noflash.mp4" type="video/mp4"></video><div id="button" class="part-of-ui absolute top-[3px] right-[1px] left-[-1px] bottom-0 opacity-10 pointer-events-none z-20 transition-all duration-75 [&amp;.hovered]:opacity-50 [&amp;.pressed]:opacity-100 [&amp;.occupied]:animate-throb [&amp;.disabled]:opacity-100 [&amp;.disabled]:grayscale occupied" data-secrets-target="buttonOverlay"><img src="https://www.thisisnotawebsitedotcom.com/assets/button.png" aria-hidden="true"></div><div id="shadow_inner" class="part-of-ui shadow-darker absolute top-0 right-0 left-0 bottom-0 z-50 pointer-events-none transition-all duration-300 !shadow-darken" data-secrets-target="shadow"></div><div id="shadow_outer" class="part-of-ui shadow-frame absolute top-[2px] right-[2px] left-[2px] bottom-[2px] z-50 pointer-events-none"></div><div name="code" type="text" class="text-2xl part-of-ui absolute bottom-[26.2%] left-[25.5%] w-[16.5%] h-[7%] bg-transparent text-white text-glow pl-[1%] pr-[3%] outline-none font-mono uppercase z-40 [&amp;.loading]:animate-loading disabled:animate-loading disabled:cursor-not-allowed" value="" data-secrets-target="field" data-action="input->secrets#inputUpdate keydown.esc->secrets#clearForm:prevent">${code}</div></div></div>`;
                element.appendChild(screen_div);
        });

        var audio_elements = document.querySelectorAll('.audio');

        audio_elements.forEach((element) => {
                element.setAttribute('controls', '');
        });
}
