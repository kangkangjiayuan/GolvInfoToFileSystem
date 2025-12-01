// 智能瞭望系统JavaScript工具函数库

/**
 * 显示提示消息
 * @param {string} message - 消息内容
 * @param {string} type - 消息类型 (success, error, warning, info)
 * @param {number} duration - 显示时长(毫秒)
 */
function showToast(message, type = 'info', duration = 3000) {
    // 创建toast容器
    let toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toast-container';
        toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
        toastContainer.style.zIndex = '9999';
        document.body.appendChild(toastContainer);
    }

    // 创建toast元素
    const toastId = 'toast-' + Date.now();
    const toast = document.createElement('div');
    toast.id = toastId;
    toast.className = `toast align-items-center text-white bg-${type} border-0 show`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;

    // 添加图标
    const iconMap = {
        'success': 'fa-check-circle',
        'error': 'fa-exclamation-circle',
        'warning': 'fa-exclamation-triangle',
        'info': 'fa-info-circle'
    };
    
    const icon = document.createElement('i');
    icon.className = `fas ${iconMap[type]} me-2`;
    toast.querySelector('.toast-body').insertBefore(icon, toast.querySelector('.toast-body').firstChild);

    // 添加到容器
    toastContainer.appendChild(toast);

    // 自动移除
    setTimeout(() => {
        const toastElement = document.getElementById(toastId);
        if (toastElement) {
            toastElement.remove();
        }
    }, duration);
}

/**
 * 显示确认对话框
 * @param {string} title - 对话框标题
 * @param {string} message - 对话框消息
 * @param {Function} onConfirm - 确认回调函数
 * @param {Function} onCancel - 取消回调函数
 */
function showConfirmDialog(title, message, onConfirm = null, onCancel = null) {
    const modalId = 'confirm-modal-' + Date.now();
    const modal = document.createElement('div');
    modal.className = 'modal fade';
    modal.id = modalId;
    modal.setAttribute('tabindex', '-1');
    modal.innerHTML = `
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">${title}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    ${message}
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">取消</button>
                    <button type="button" class="btn btn-primary" id="confirm-btn">确认</button>
                </div>
            </div>
        </div>
    `;

    document.body.appendChild(modal);
    
    const bsModal = new bootstrap.Modal(modal);
    bsModal.show();

    // 绑定确认按钮事件
    document.getElementById('confirm-btn').addEventListener('click', function() {
        if (onConfirm) onConfirm();
        bsModal.hide();
        modal.remove();
    });

    // 绑定取消事件
    modal.addEventListener('hidden.bs.modal', function() {
        if (onCancel) onCancel();
        modal.remove();
    });
}

/**
 * 复制到剪贴板
 * @param {string} text - 要复制的文本
 * @param {string} message - 成功提示消息
 */
function copyToClipboard(text, message = '已复制到剪贴板') {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(function() {
            showToast(message, 'success');
        }).catch(function(err) {
            console.error('复制失败:', err);
            showToast('复制失败', 'error');
        });
    } else {
        // 降级方案
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        try {
            document.execCommand('copy');
            showToast(message, 'success');
        } catch (err) {
            console.error('复制失败:', err);
            showToast('复制失败', 'error');
        }
        document.body.removeChild(textArea);
    }
}

/**
 * 格式化文件大小
 * @param {number} bytes - 字节数
 * @returns {string} 格式化后的大小
 */
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

/**
 * 格式化日期时间
 * @param {Date|string} date - 日期对象或日期字符串
 * @param {string} format - 格式字符串
 * @returns {string} 格式化后的日期时间
 */
function formatDateTime(date, format = 'YYYY-MM-DD HH:mm:ss') {
    const d = new Date(date);
    const year = d.getFullYear();
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const day = String(d.getDate()).padStart(2, '0');
    const hours = String(d.getHours()).padStart(2, '0');
    const minutes = String(d.getMinutes()).padStart(2, '0');
    const seconds = String(d.getSeconds()).padStart(2, '0');

    return format
        .replace('YYYY', year)
        .replace('MM', month)
        .replace('DD', day)
        .replace('HH', hours)
        .replace('mm', minutes)
        .replace('ss', seconds);
}

/**
 * 防抖函数
 * @param {Function} func - 要执行的函数
 * @param {number} wait - 等待时间(毫秒)
 * @returns {Function} 防抖后的函数
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * 节流函数
 * @param {Function} func - 要执行的函数
 * @param {number} limit - 限制时间(毫秒)
 * @returns {Function} 节流后的函数
 */
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

/**
 * 显示加载动画
 * @param {string} containerId - 容器ID
 * @param {string} message - 加载消息
 */
function showLoading(containerId, message = '加载中...') {
    const container = document.getElementById(containerId);
    if (!container) return;

    container.innerHTML = `
        <div class="text-center py-5">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">${message}</span>
            </div>
            <p class="mt-3 text-muted">${message}</p>
        </div>
    `;
}

/**
 * 隐藏加载动画
 * @param {string} containerId - 容器ID
 */
function hideLoading(containerId) {
    const container = document.getElementById(containerId);
    if (container) {
        container.innerHTML = '';
    }
}

/**
 * AJAX请求封装
 * @param {string} url - 请求URL
 * @param {object} options - 请求选项
 * @returns {Promise} Promise对象
 */
function ajaxRequest(url, options = {}) {
    const defaultOptions = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        },
        timeout: 30000
    };

    const mergedOptions = { ...defaultOptions, ...options };

    return fetch(url, mergedOptions)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            return response.json();
        })
        .catch(error => {
            console.error('请求失败:', error);
            showToast('请求失败: ' + error.message, 'error');
            throw error;
        });
}

/**
 * 表单验证
 * @param {HTMLFormElement} form - 表单元素
 * @param {object} rules - 验证规则
 * @returns {boolean} 验证结果
 */
function validateForm(form, rules = {}) {
    let isValid = true;
    const errors = {};

    // 清除之前的错误提示
    form.querySelectorAll('.is-invalid').forEach(element => {
        element.classList.remove('is-invalid');
    });

    // 验证必填字段
    form.querySelectorAll('[required]').forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            errors[field.name] = '此字段为必填项';
            isValid = false;
        }
    });

    // 验证邮箱格式
    const emailFields = form.querySelectorAll('input[type="email"]');
    emailFields.forEach(field => {
        if (field.value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(field.value)) {
            field.classList.add('is-invalid');
            errors[field.name] = '请输入有效的邮箱地址';
            isValid = false;
        }
    });

    // 验证密码长度
    const passwordFields = form.querySelectorAll('input[type="password"]');
    passwordFields.forEach(field => {
        if (field.value && field.value.length < 6) {
            field.classList.add('is-invalid');
            errors[field.name] = '密码长度至少为6位';
            isValid = false;
        }
    });

    // 显示错误信息
    if (!isValid) {
        Object.keys(errors).forEach(fieldName => {
            const field = form.querySelector(`[name="${fieldName}"]`);
            if (field) {
                const feedback = field.parentNode.querySelector('.invalid-feedback');
                if (feedback) {
                    feedback.textContent = errors[fieldName];
                }
            }
        });
    }

    return isValid;
}

/**
 * 页面加载动画
 */
function pageLoadAnimation() {
    // 为页面元素添加渐入动画
    const animatedElements = document.querySelectorAll('.fade-in, .fade-in-left, .fade-in-right');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0) translateX(0)';
            }
        });
    });

    animatedElements.forEach(element => {
        element.style.opacity = '0';
        element.style.transform = element.classList.contains('fade-in-left') ? 
            'translateX(-30px)' : element.classList.contains('fade-in-right') ? 
            'translateX(30px)' : 'translateY(30px)';
        element.style.transition = 'all 0.6s ease-out';
        observer.observe(element);
    });
}

/**
 * 初始化页面功能
 */
function initializePage() {
    // 页面加载动画
    pageLoadAnimation();

    // 为所有表单添加验证
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
                return false;
            }
        });
    });

    // 为所有复制按钮添加点击事件
    document.querySelectorAll('[data-copy]').forEach(button => {
        button.addEventListener('click', function() {
            const text = this.getAttribute('data-copy');
            copyToClipboard(text);
        });
    });

    // 为所有工具提示添加事件
    document.querySelectorAll('[data-tooltip]').forEach(element => {
        element.classList.add('tooltip-custom');
    });

    console.log('页面初始化完成');
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', initializePage);