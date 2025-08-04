// Fix para prevenir errores de selectores CSS inválidos
(function() {
    'use strict';
    
    // Sobrescribir querySelector para manejar selectores inválidos
    const originalQuerySelector = Document.prototype.querySelector;
    const originalQuerySelectorAll = Document.prototype.querySelectorAll;
    
    Document.prototype.querySelector = function(selector) {
        try {
            return originalQuerySelector.call(this, selector);
        } catch (e) {
            console.warn('Selector CSS inválido ignorado:', selector, e.message);
            return null;
        }
    };
    
    Document.prototype.querySelectorAll = function(selector) {
        try {
            return originalQuerySelectorAll.call(this, selector);
        } catch (e) {
            console.warn('Selector CSS inválido ignorado:', selector, e.message);
            return document.createDocumentFragment();
        }
    };
    
    // También para elementos
    const originalElementQuerySelector = Element.prototype.querySelector;
    const originalElementQuerySelectorAll = Element.prototype.querySelectorAll;
    
    Element.prototype.querySelector = function(selector) {
        try {
            return originalElementQuerySelector.call(this, selector);
        } catch (e) {
            console.warn('Selector CSS inválido ignorado:', selector, e.message);
            return null;
        }
    };
    
    Element.prototype.querySelectorAll = function(selector) {
        try {
            return originalElementQuerySelectorAll.call(this, selector);
        } catch (e) {
            console.warn('Selector CSS inválido ignorado:', selector, e.message);
            return document.createDocumentFragment();
        }
    };
    
    console.log('🛡️ Protección contra selectores CSS inválidos activada');
})();
