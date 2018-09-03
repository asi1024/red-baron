import Control.Monad

main = do
  x <- liftM read getLine :: IO Int
  putStrLn $ show (x * x * x)
