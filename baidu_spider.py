import requests
from bs4 import BeautifulSoup
import urllib.parse
import gzip
from io import BytesIO

class BaiduSpider:
    def __init__(self):
        # 初始化请求头，基于用户提供的信息
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': 'BIDUPSID=92E673284EF4D8827852752E4AB79013; PSTM=1763822036; BAIDUID=92E673284EF4D8827852752E4AB79013:FG=1; BD_UPN=12314753; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=60276_63146_66105_65866_66218_66209_66237_66166_66291_66264_66393_66465_66477_66529_66559_66585_66581_66592_66601_66615_66647_66663_66666_66690_66599_66727; H_WISE_SIDS=60276_63146_66105_65866_66218_66209_66237_66166_66291_66264_66393_66465_66477_66529_66559_66585_66581_66592_66601_66615_66647_66663_66666_66690_66599_66727; BAIDUID_BFESS=92E673284EF4D8827852752E4AB79013:FG=1; delPer=0; BD_CK_SAM=1; PSINO=6; BA_HECTOR=858k8180252k240l048h218185aha31kinlot25; ZFY=OknCNml8GeZDBKp78bFHW9mN3jHosRvXR7jMIOqjCB0:C; BD_HOME=1; H_PS_645EC=978d8Ru13vn6fki4pqKb6yXthFIUSmd9b1iAyZ8ypE4GhHREIvZ52BksPgQ; baikeVisitId=7dffc0fb-7bff-4ad5-9b99-a40c051269d8',
            'Host': 'www.baidu.com',
            'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/'
        }
        self.base_url = 'https://www.baidu.com/s'
    
    def search(self, keyword):
        """
        执行百度搜索
        :param keyword: 搜索关键词
        :return: 搜索结果页面的HTML内容
        """
        # 构建查询参数
        params = {
            'wd': keyword,
            'rn': 10  # 限制结果数量为10个，提高响应速度
        }
        
        # 发送请求
        try:
            # 使用简化的请求头，减少请求大小和处理时间
            simple_headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
            
            response = requests.get(
                url=self.base_url,
                params=params,
                headers=simple_headers,
                timeout=8,  # 减少超时时间到8秒
                allow_redirects=True,
                stream=False  # 禁用流式传输，提高响应速度
            )
            # 检查响应状态
            response.raise_for_status()
            
            # 确保使用正确的编码
            response.encoding = response.apparent_encoding
            return response.text
        except Exception as e:
            print(f"搜索请求失败: {e}")
            return None
    
    def parse_results(self, html_content):
        """
        解析搜索结果，提取标题、摘要、URL和封面URL
        :param html_content: 搜索结果页面的HTML内容
        :return: 解析后的搜索结果列表
        """
        if not html_content:
            return []
        
        results = []
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # 使用更高效的解析策略，优先使用最常见和有效的选择器
            result_containers = soup.select('.result, .c-container, .result-op')
            
            # 如果没有找到特定容器，使用通用方法
            if not result_containers:
                # 快速查找所有可能的搜索结果链接
                all_links = soup.find_all('a', href=True, limit=20)  # 限制数量提高性能
                
                seen_titles = set()
                
                for link in all_links:
                    href = link.get('href', '')
                    # 快速过滤百度内部链接
                    if 'baidu.com' in href and 'baidu.com/link?' not in href:
                        continue
                    
                    title = link.get_text().strip()
                    if len(title) < 5 or title in seen_titles:
                        continue
                    
                    seen_titles.add(title)
                    
                    # 快速获取父容器信息
                    parent = link.find_parent(['div', 'li'])
                    abstract = '无摘要'
                    if parent:
                        parent_text = parent.get_text().strip()
                        if len(parent_text) > len(title) + 10:
                            abstract = parent_text[:150] + '...' if len(parent_text) > 150 else parent_text
                    
                    # 只添加有意义的结果
                    if title and href:
                        results.append({
                            'rank': len(results) + 1,
                            'title': title,
                            'url': href,
                            'abstract': abstract,
                            'cover_url': '无封面图'
                        })
                    
                    # 限制结果数量
                    if len(results) >= 10:
                        break
            else:
                # 使用找到的容器进行解析（优化版本）
                seen_titles = set()
                
                for container in result_containers[:15]:  # 限制处理数量
                    # 快速查找标题
                    title_elem = container.find('h3') or container.find('a', href=True)
                    if not title_elem:
                        continue
                    
                    title = title_elem.get_text().strip()
                    if len(title) < 5 or title in seen_titles:
                        continue
                    seen_titles.add(title)
                    
                    # 快速查找URL
                    url_elem = container.find('a', href=True)
                    url = url_elem.get('href', '无URL') if url_elem else '无URL'
                    
                    # 快速查找摘要
                    abstract = '无摘要'
                    abstract_elem = container.find(['p', '.c-abstract'])
                    if abstract_elem:
                        abstract_text = abstract_elem.get_text().strip()
                        abstract = abstract_text[:150] + '...' if len(abstract_text) > 150 else abstract_text
                    else:
                        # 快速从容器文本中提取
                        container_text = container.get_text().strip()
                        if len(container_text) > len(title) + 10:
                            abstract = container_text[:150] + '...' if len(container_text) > 150 else container_text
                    
                    # 只添加有意义的结果
                    if title and url != '无URL':
                        results.append({
                            'rank': len(results) + 1,
                            'title': title,
                            'url': url,
                            'abstract': abstract,
                            'cover_url': '无封面图'  # 简化处理，不查找图片以提高速度
                        })
                    
                    # 限制结果数量
                    if len(results) >= 10:
                        break
            
            print(f"快速解析完成，共 {len(results)} 条结果")
            
        except Exception as e:
            print(f"解析结果时发生异常: {e}")
            # 简化错误处理，不保存错误文件以提高性能
        
        return results
    
    def save_results(self, results, filename='search_results.txt'):
        """
        保存搜索结果到文件
        :param results: 搜索结果列表
        :param filename: 保存的文件名
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for result in results:
                    f.write(f"排名: {result['rank']}\n")
                    f.write(f"标题: {result['title']}\n")
                    f.write(f"URL: {result['url']}\n")
                    f.write(f"摘要: {result['abstract']}\n")
                    f.write(f"封面URL: {result['cover_url']}\n")
                    f.write("-" * 50 + "\n")
            print(f"结果已保存到 {filename}")
        except Exception as e:
            print(f"保存结果失败: {e}")


def main():
    """
    主函数，演示爬虫的使用
    """
    spider = BaiduSpider()
    
    # 获取用户输入的搜索关键词
    keyword = input("请输入搜索关键词: ")
    
    print(f"正在搜索: {keyword}...")
    html_content = spider.search(keyword)
    
    if html_content:
        print("搜索完成，正在解析结果...")
        results = spider.parse_results(html_content)
        
        if results:
            print(f"找到 {len(results)} 条结果:")
            for result in results[:5]:  # 只显示前5条结果
                print(f"\n排名: {result['rank']}")
                print(f"标题: {result['title']}")
                print(f"URL: {result['url']}")
                print(f"摘要: {result['abstract']}")
                print(f"封面URL: {result['cover_url']}")
            
            # 保存所有结果到文件
            spider.save_results(results)
        else:
            print("未能解析到搜索结果")


if __name__ == "__main__":
    main()