# Testing C++ code with Haskell

## Howto

1. Declare functions you want to test as `extern` in the C++ header files

    ```c
    extern "C" int addNum(int, int);
    
    int addNum(int, int);
    ```

2. Compile as static library (`.o` file)

    ```bash
    $ g++ -c addnum.cpp
    $ ls *.o
    addnum.o
    $
    ```

3. Import into haskell with FFI and create `Arbitrary` instance

    ```haskell
    import Test.QuickCheck
    import Foreign
    import Foreign.C.Types

    instance Arbitrary CInt where
        arbitrary = fmap CInt arbitrary
    
    
    foreign import ccall "addnum.h addNum"
        c_addNum :: CInt -> CInt -> CInt
    
    prop_c_addNum :: CInt -> CInt -> Bool
    prop_c_addNum x y = x+y == c_addNum x y
    ```

4. Start ghci with `-lstdc++`
    
    ```
    $ ghci -lstdc++ addnum.o
    ..
    Loading object (static) addnum.o ... done
    ..
    λ> :l addNum.hs
    ..
    Ok, modules loaded: Main.
    λ> quickCheck prop_c_addNum
    ..
    +++ OK, passed 100 tests.
    ```

## Links

http://blog.coldflake.com/posts/2012-10-11-quickcheck-testing-c%2B%2B.html
