module Neuron where


type ID = Int

data Neuron = Neuron ID (Double -> Double) Axion

data Axion = Axion ID [Neuron] [Double] | Nil
    deriving (Show)


instance Show Neuron where
    show (Neuron id f a) = "Neuron " ++ show id ++ " with Connections: " ++ show a






testNeuron = Neuron 3 (*3) Nil
testAxion = Axion 15 [testNeuron] [2]
