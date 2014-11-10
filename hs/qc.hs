{-# LANGUAGE GeneralizedNewtypeDeriving #-}

import Test.QuickCheck
import Foreign
import Foreign.C.Types

-- Haskell usage of QuickCheck
prop_doublerev :: String -> Bool
prop_doublerev xs = xs == reverse (reverse xs)

prop_revapp :: [Int] -> [Int] -> Bool
prop_revapp xs ys = reverse (xs++ys) == reverse ys ++ reverse xs

-- Talking to a C++ program
instance Arbitrary CInt where
    arbitrary = choose (-1000,1000)
--newtype CIntT = CUIntT Int deriving (Arbitrary,Eq,Num,Show)

foreign import ccall "qc_testables.h addNum"
    c_addNum :: CInt -> CInt -> CInt

prop_cAddNum :: CInt -> CInt -> Bool
prop_cAddNum x y = x+y == c_addNum x y
