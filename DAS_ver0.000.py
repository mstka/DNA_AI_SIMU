import tensorflow as tf
import numpy as np

class AI:
    def __init__(self, input_nodes, output_nodes, hidden_layers):
        """
        入力ノード数、出力ノード数、中間層の層数とノード数をリストで指定してモデルを構築。
        
        input_nodes: 入力層のノード数（整数）
        output_nodes: 出力層のノード数（整数）
        hidden_layers: 中間層のノード数をリストで指定
        """
        self.input_nodes = input_nodes
        self.output_nodes = output_nodes
        self.hidden_layers = hidden_layers

        # モデルを構築
        self.model = self.build_model()

        # 最適化器
        self.optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
    
    def build_model(self):
        """
        モデルの構築: 入力層、隠れ層、出力層を作成
        """
        model = tf.keras.Sequential()
        
        # 入力層
        model.add(tf.keras.layers.InputLayer(input_shape=(self.input_nodes,)))
        
        # 隠れ層
        for nodes in self.hidden_layers:
            model.add(tf.keras.layers.Dense(nodes, activation='relu'))
        
        # 出力層
        model.add(tf.keras.layers.Dense(self.output_nodes, activation='linear'))
        
        return model
    
    def predict(self, state):
        """
        状態に対する予測を行う
        """
        return self.model(state)
    
    def train(self, state, reward):
        """
        報酬に基づいてモデルを更新（強化学習の学習）。
        
        state: 現在の状態（NumPy配列またはテンソル）
        reward: 現在の報酬（実数）
        """
        with tf.GradientTape() as tape:
            # 予測値を計算
            predictions = self.model(state)
            
            # 損失関数を定義（報酬に基づいて学習）
            # ここではMSE（平均二乗誤差）を使って、予測値が報酬に近づくように調整
            loss = tf.reduce_mean(tf.square(predictions - reward))
        
        # 勾配を計算して最適化
        grads = tape.gradient(loss, self.model.trainable_variables)
        self.optimizer.apply_gradients(zip(grads, self.model.trainable_variables))
        
        return loss.numpy()

# 使用例

if __name__ == "__main__":
    # AIのモデル設定（入力ノード数、出力ノード数、中間層のノード数）
    input_nodes = 4
    output_nodes = 2
    hidden_layers = [10, 10]  # 2つの中間層（それぞれ10ノード）

    # AIインスタンスを作成
    ai = AI(input_nodes, output_nodes, hidden_layers)

    # 仮想的な状態を作成（4次元の入力）
    state = np.random.rand(1, input_nodes).astype(np.float32)

    # 報酬（仮に実数）
    reward = np.array([1.0])

    # 学習を実行
    loss = ai.train(state, reward)
    print(f"Training Loss: {loss}")
