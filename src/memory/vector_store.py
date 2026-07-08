"""
向量存储模块：基于 ChromaDB 或 FAISS 实现文档检索与记忆功能
用于存储和检索历史对话、科学文献、分析结果等
"""
import os
import json
import numpy as np
from typing import List, Dict, Any, Optional, Tuple


class VectorStore:
    """
    轻量级向量存储（支持 ChromaDB 和 FAISS）
    若未安装 ChromaDB，自动降级为内存字典存储
    """
    def __init__(self, collection_name: str = "climate_memory", persist_dir: str = "outputs/memory"):
        self.collection_name = collection_name
        self.persist_dir = persist_dir
        self.use_chroma = False
        self.collection = None
        self._initialize()

    def _initialize(self):
        """初始化向量数据库"""
        try:
            import chromadb
            from chromadb.config import Settings
            
            # 确保持久化目录存在
            os.makedirs(self.persist_dir, exist_ok=True)
            
            self.client = chromadb.PersistentClient(
                path=self.persist_dir,
                settings=Settings(anonymized_telemetry=False)
            )
            
            # 获取或创建集合
            try:
                self.collection = self.client.get_collection(self.collection_name)
            except:
                self.collection = self.client.create_collection(
                    name=self.collection_name,
                    metadata={"hnsw:space": "cosine"}
                )
            
            self.use_chroma = True
            print(f"✅ ChromaDB 已初始化: {self.collection_name}")
            
        except ImportError:
            print("⚠️ ChromaDB 未安装，使用内存模式（数据不会持久化）")
            print("   安装: pip install chromadb")
            self.use_chroma = False
            self._memory_store = []  # 内存存储
            self._id_counter = 0

    def add_document(
        self,
        text: str,
        metadata: Optional[Dict[str, Any]] = None,
        embedding: Optional[np.ndarray] = None
    ) -> str:
        """
        添加文档到向量库
        :param text: 文档内容
        :param metadata: 元数据（如来源、时间等）
        :param embedding: 若提供则直接使用，否则需自行生成（此处暂用文本替代）
        :return: 文档ID
        """
        if metadata is None:
            metadata = {}

        doc_id = f"doc_{len(self._memory_store) if not self.use_chroma else self.collection.count()}"

        if self.use_chroma and embedding is not None:
            # 使用 ChromaDB
            self.collection.add(
                ids=[doc_id],
                documents=[text],
                metadatas=[metadata],
                embeddings=[embedding.tolist()]
            )
        else:
            # 内存模式
            self._memory_store.append({
                "id": doc_id,
                "text": text,
                "metadata": metadata,
                "embedding": embedding
            })
            self._id_counter += 1

        return doc_id

    def search(
        self,
        query: str,
        top_k: int = 5,
        embedding: Optional[np.ndarray] = None
    ) -> List[Dict[str, Any]]:
        """
        检索最相似的文档
        :param query: 查询文本
        :param top_k: 返回数量
        :param embedding: 若提供则直接使用
        :return: 相似文档列表
        """
        if self.use_chroma:
            # 使用 ChromaDB 检索
            results = self.collection.query(
                query_texts=[query],
                n_results=top_k
            )
            
            # 格式化结果
            documents = []
            if results and results['ids']:
                for i in range(len(results['ids'][0])):
                    documents.append({
                        "id": results['ids'][0][i],
                        "text": results['documents'][0][i],
                        "metadata": results['metadatas'][0][i] if results['metadatas'] else {},
                        "distance": results['distances'][0][i] if results['distances'] else None
                    })
            return documents
        
        else:
            # 内存模式：简单文本匹配（实际应使用嵌入相似度）
            print("⚠️ 内存模式使用关键词匹配，建议安装 chromadb 以获得更好的检索效果")
            results = []
            for doc in self._memory_store:
                if query.lower() in doc['text'].lower():
                    results.append(doc)
            return results[:top_k]

    def get_all_documents(self) -> List[Dict[str, Any]]:
        """获取所有文档（用于调试）"""
        if self.use_chroma:
            results = self.collection.get()
            documents = []
            if results and results['ids']:
                for i in range(len(results['ids'])):
                    documents.append({
                        "id": results['ids'][i],
                        "text": results['documents'][i] if results['documents'] else "",
                        "metadata": results['metadatas'][i] if results['metadatas'] else {}
                    })
            return documents
        else:
            return self._memory_store

    def clear(self):
        """清空所有文档"""
        if self.use_chroma:
            self.client.delete_collection(self.collection_name)
            self.collection = self.client.create_collection(self.collection_name)
        else:
            self._memory_store = []
            self._id_counter = 0
        print(f"🗑️ 已清空集合: {self.collection_name}")