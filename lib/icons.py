import wx
is_wxPhoenix = 'phoenix' in wx.PlatformInfo
from wx.lib.embeddedimage import PyEmbeddedImage
import base64

RAW_ICONS = {
"nn": """iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAIAAABvFaqvAAAACXBIWXMAAAxMAAAMTAEAiU+qAAAACXZwQWcAAAAYAAAAGAB4TKWmAAAB3klEQVQ4y+2VMW7bQBBF/3CHkhrFCFwlKV2l9gF8Al8k6dy5IkEV7twld1GlE1gG3aRymVAuXBiGERq7Mz8FEUoiBQRIm/yKnP3zwJmd5UprVAGJPQlAmHGay6fP3wF8/fLhNTIE6Zb2vIJEIDrHcqcZSS6qBrgFbhdVQ9KMfsgfnYh2gJKSkyzLBliHUIdQA+uybEim5GNWtBHInTE6yaLoKHcitUgdwh2wLoqGZIxD1hDkzpQ4oAA1MGSltFfjHmhQkWrdU3qW6uEaozHrOk/CjCFIUWzKsglBzYZbScIMIWhZNkWxCUHM2HsyCEiIQFUWi4eq2kwmKoIsw1hZBhFMJlpVm8XiQVWkGx2BRGMQxMjLyx/X1w2gO3MSRijbmbR0cfHu6up9nosR6g5VLJfPq9XL2dlbd5AIAa+vvLn5GeO2vDyX09P5dCpm6D55tXpZLp/Pz9+4QaJRM7Stz2Z7xTw9+cnJt8fHJCIASB4f6/39x6OjPVuXmBzavc9mmfu2qSJoWx83u219Ps86Q5/YPehu8m5Tu74OzlQXd98u9YnamwaSceh3UOSA/9Am/5X+g/5pkEL+4BheMAclUCNk1y2gIw9wQFVCkDzPAMToqtIdx+SQbPuzEYERvwBwYMALE1tK0wAAACV0RVh0Y3JlYXRlLWRhdGUAMjAxMC0xMS0xMlQxMTozNDo0NS0wNjowMF4RciAAAAAldEVYdG1vZGlmeS1kYXRlADIwMTAtMTEtMTJUMTA6NDc6MzEtMDY6MDDgsF4bAAAAHXRFWHRTb2Z0d2FyZQBHUEwgR2hvc3RzY3JpcHQgOC43MQM/aDQAAAAASUVORK5CYII=""",
"ss": """iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAIAAABvFaqvAAAACXBIWXMAAAxMAAAMTAEAiU+qAAAACXZwQWcAAAAYAAAAGAB4TKWmAAAB4UlEQVQ4y+2Vv3LTQBDGv72TYleuPDiBB6BheI40eRHo0qWQ5NhFunTwMnkHZ+yhoaEDAePKQ2HrbvejOFuOZTOhh280o9H++d3tanWStTITkNhKQEPu8XOpb998Xi5jnjsAIdhwmC0+vX4x9EEhDtiliCASmRd4AQSt6ADAATFSlaqWzDEmDzIH6aQArgX/SSIQeSYGhHsu5G/1H/RPg7J045OxJCEC8sSkJmPHk8Y1ax/M9iAzmHUTTtrdrqQtaL22fv+gzH7fdb4MEfT7zh02o03MzACHh4dfVfV9MPBpQe+x2XC1MkB268tqZZeXX3o9UYUInMNqpbe351dXAzNIUHpBCLy5+XZ/XwPZ/oCAP+qStvsD4vX1xd3dyzwXJSQY/a5h0+mPsqzPztK+qNrFeA8RcQ5No5PJRVGMUu80HSMiIBEji2JUludNE1Nfj5UKb5pYludFMYqR6RWDQFAmmTFGIzke18Asy+Yic2B/icyzbA7MxuOaZIxmts0Nyj1oxyLJqqqBmfeLliUy934BzKoqUdhSToASKwTrsDqUEOwp5TTouEbv596frugQdGRNLFWSnE5q4BF4nE5qkqq0U/HBKN3fUTslhCp7ubx7/xXAxw+vNoHeS3J1Jj4SvwHUp92N41HPcAAAACV0RVh0Y3JlYXRlLWRhdGUAMjAxMC0xMS0xMlQxMTozNDo0NS0wNjowMF4RciAAAAAldEVYdG1vZGlmeS1kYXRlADIwMTAtMTEtMTJUMTA6NDc6NDUtMDY6MDAeOnMRAAAAHXRFWHRTb2Z0d2FyZQBHUEwgR2hvc3RzY3JpcHQgOC43MQM/aDQAAAAASUVORK5CYII=""",
"sw": """iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAIAAABvFaqvAAAACXBIWXMAAAxMAAAMTAEAiU+qAAAACXZwQWcAAAAYAAAAGAB4TKWmAAACWklEQVQ4y42VTU4bQRCFX1XbFmNbipULOAfhEKzsJXgBghslIMsjFthmiVhGiVAOwIyl7IOXUcCgBPwz0/WyGMd2sIEpjUat/vn6ve7qbpl4FgQkcoYIvAcA5+ajRJASBSdwAkhekBlKhXnB6bySgCK3FgBJQlWE4ajXu1dFknBJSjxzxmxmJHu9UbEYlcvxxcUDySQxkolnXlA2oN8fVauRSCwS12rx5eUDSTOmlg+00BIEERCJxKqxSFypxN3uiOQ0oeZZl2JRer37VutmPBZVJUFCBEli06nN+6VG8zkdRc4NgNi5gUhUrUbn56OltVlCkmn6tiPVARBn/yCIMlOzmdGYeOLr1Z9PH39lVWbPKd1uRolXKFEQRL3eaNFnvmufv/x27joMb0mmqeVx1O+PFn2WoKtvjypRqXTd6dxmk0yn+RytLmVmzblYNS4Wr9vt26zh7CyXo1VQAQCN6iRN9ehoWKno1pbs799MJnBOvKdzYmbVKtrteqNRS1MWixtOZiE70t5DRGYzabWGqnh8hKp6T1XxnkGAk5N6o1HLcmpjuhX+nTmhUUTG4+xmEDOKiJkFATqderP5GgXASmbLPF9FQEIVgJXLDMN6s/mio2eKlrG4q0hUq3J6+mFn593rWtYUrYUZJhNm9Dev0M2gbNjTE3d3f4ThXakkZm+QCtnSbmwT0TTl4eEQwN7e+zRh4WWD810TkXXxJNUhSfTgYM7yHqrYOK+KwAgaBRDw/w/0FAEprdbw+Phu8XKsiYf8vEu/DyYEXvAHAk5lOjXnZHu7ss7KnqO/bT27tA7euksAAAAldEVYdGNyZWF0ZS1kYXRlADIwMTAtMTEtMTJUMTE6MzQ6NDUtMDY6MDBeEXIgAAAAJXRFWHRtb2RpZnktZGF0ZQAyMDEwLTExLTEyVDEwOjQ3OjA5LTA2OjAwXdAXnwAAAB10RVh0U29mdHdhcmUAR1BMIEdob3N0c2NyaXB0IDguNzEDP2g0AAAAAElFTkSuQmCC""",
"ne": """iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAIAAABvFaqvAAAACXBIWXMAAAxMAAAMTAEAiU+qAAAACXZwQWcAAAAYAAAAGAB4TKWmAAACX0lEQVQ4y42UMU/bQBzF3//ONjiJVJoPEDp0q9SvwoaQGGIGCJ8JBpMBJc6IGKtWqOzYjFWlCnYEqASSnO9eB4c0pknqJ8uy5Hc/v3d3PhlZegIS8xKBtbi8HFrLtTVlHQWLRUKAT5/XPS3QApSNziHw8PPHuNO59TwhhY6AACx/T0gS+HbxUZVflRIdHDTjuCVCEqKFACHlC6JECUiohYFFoDVywyhqHh21fN/RQWRBPxJFHQ/L5fliLaOoCaDTuTVGAOGCBgSWJJpJKZlMGEXNbvdDrSZF2MXO1SCR6cj1dVErvf8B5Tl9XwaDh93dX09PFAH5l14VZAw9T5LkIYpunp8FUM6hYBW4+RVXKyi+L/3+w97ezcuLKKVIKiUk63WEIUiKKoLJUtCs0f7+zWgErcU5ai2kq9dxeroZx60gIEmtp6vmLcuSJEUWKKWspVJiLcMQx8ebW1vvAAyHrcPDW2vVNJexnNdk4kj2evdhmAKZUtev9zQM037/nuR47ApbHN8FwZWS9OL7sAQyxpFMkvtGIxVJtb4GMq2vRdJGI02S+5mHZJ47kicnd1pfffn626veaHt7o/DM9qoxbLeb4xG1FhhLukqNCs8b5TlJTgyROzpHkoNBpUb/ylnmjhgbkux274LgSqlMJJslCsO011uaZV7GcrqPgkD5vpptf+dcGDKON3d2SvOy8m96rXZ+/rixkYlkIlmVRm8STZe/GHB29lirZb6/anaXgcRYeqq0/KMR2+33VRtNa0GMo/fqdw7FoTN7qAoiPEvI9OiFCCY5AGiN3FWliMASfwDgYH5MXi5Z8wAAACV0RVh0Y3JlYXRlLWRhdGUAMjAxMC0xMS0xMlQxMTozNDo0NS0wNjowMF4RciAAAAAldEVYdG1vZGlmeS1kYXRlADIwMTAtMTEtMTJUMTA6NDY6NTYtMDY6MDAMugIsAAAAHXRFWHRTb2Z0d2FyZQBHUEwgR2hvc3RzY3JpcHQgOC43MQM/aDQAAAAASUVORK5CYII=""",
"ww": """iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAIAAABvFaqvAAAACXBIWXMAAAxMAAAMTAEAiU+qAAAACXZwQWcAAAAYAAAAGAB4TKWmAAAB3UlEQVQ4y6VVO27bUBCc/YiFgcBllDZXsK+U3gewxI9dJQjgs9iNG3eukhOkD0DGCAzIQGBZfLubgpIiyw7JIFM+koOZnTdLWlooIQJ7IMAczBgEEVJAhSAE0LNnHa2MYNm+z3ihJQIIWIqrq4fl0tcng0ytxS7co209Ik5Ovh8ff3MPs3CPfrQWvKfFHap0dvbj4qI+OBCiIS0b8HOWEEFZNvN5zaxjOQAQdMtiFqqU501V1Vmmq1Vy34xscEQBBf1xVBRNVdUi2n3c+RIZJpoQFIFAiFBVNWVZq4rZWkPbxmLhT09OBOqdlgXoaeXZhIqiKctaRN1j62UyocNDjkAEengikGVEEXF+3sxm+yw7N2QYqiR3Pz98+ninKu6vFWUcsmxMl8ZBvn75LIKbmwd5PZ5R1gDoqo3T02lK+MuwZeSwlYXcoyimzMjzLn4ww8yOjt5cX78fGb+CQCAzzOdT97UuZpit49+tUZ81BIjBjJSiKKYR6C43NuUwAxH625ti0zUiiJBZlOWUGUXRMFMXacfST0S7sonATGbI82lVvXNP/xD+VtEOF1KK2ezt/X26vf01pvpr7G3Ibkl2e/LycvH4aN3J4Iak1kPppdK185FIAbUA4X9/Rxb4DQ6meRDp8UWOAAAAJXRFWHRjcmVhdGUtZGF0ZQAyMDEwLTExLTEyVDExOjM0OjQ1LTA2OjAwXhFyIAAAACV0RVh0bW9kaWZ5LWRhdGUAMjAxMC0xMS0xMlQxMDo0Nzo0MS0wNjowMOp1VwIAAAAddEVYdFNvZnR3YXJlAEdQTCBHaG9zdHNjcmlwdCA4LjcxAz9oNAAAAABJRU5ErkJggg==""",
"ee": """iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAIAAABvFaqvAAAACXBIWXMAAAxMAAAMTAEAiU+qAAAACXZwQWcAAAAYAAAAGAB4TKWmAAABxklEQVQ4y61VS04bQRSs1/0MiDUoM/fgEBwlyooDWPOxL8BZ4BJsoyiLbLKKZEhWThaYmX6vshgDNgZPR6RWLc1Tqaq6+o2sjCogMQp3xIDdQREkQqMgCiDjRHhk2Z3l88e3MYhdrfz6+rclgq/JJ9Ab98OdZnTn2dm3i4sfJPve3bdmemPIsLQO4vg4Xl4u5vM7VXF/qStkpfM0HbSqFm17GyPcucml5EhKfAzFHe48ONCmWbijbYuUGKOIAIBOxsyJbB1IxKiz2UIETVOYIQRAoHe/LO51R5LE4WHoewJwpztUY9suQkBVFe4ERIria9dRZA8RRCCC5dIHrkFdCGKW6rpsmqLrKaqfU8roNfCiiU9c83k5nRZydPTl4cFzaHZ7KIIYYeYfP53m9mgUmtJ2H/7RWkpra3pyou8Mezotup5y+zNlXv/5+febmz8xRnfEiJSsbcvh+h2iH05jZgqTiQAIQQCklOq6rKqhkAJAe4eOKBravL41EZilqiqbZuOJOHTwn4MQEIJ0nTVNWdeF2fNDQ85i24R7ms0GFoQgWwr+12LLIiJ5f29XV8uB4gXLQCS9U7N321vLPxFqhOC9vyMj/gJsaMELYgNmYQAAACV0RVh0Y3JlYXRlLWRhdGUAMjAxMC0xMS0xMlQxMTozNDo0NS0wNjowMF4RciAAAAAldEVYdG1vZGlmeS1kYXRlADIwMTAtMTEtMTJUMTA6NDc6MzYtMDY6MDAlF2CVAAAAHXRFWHRTb2Z0d2FyZQBHUEwgR2hvc3RzY3JpcHQgOC43MQM/aDQAAAAASUVORK5CYII=""",
"camera": """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""",
"se": """iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAIAAABvFaqvAAAACXBIWXMAAAxMAAAMTAEAiU+qAAAACXZwQWcAAAAYAAAAGAB4TKWmAAACaUlEQVQ4y5WVwW4TSRCG/796xsGOD34DhDgi8TjADRkEgjcCJMRcgiccEcfdZaPlnpk8wTrnTRwExo57un4O4xgTQuwtjUatUc1X9Vd3VXOelBESAJBICQBCWH7Zxkg0QhaIQIAA4I5OtlwE2xYEQIDhInKMMkNZnhXFxAwxbp1SS4pJkmJ0Se/ff+716jyvynIiabFwbWcxCY3LXZI+fPg8GNRkTdb9frW/P1kF2Ap0HiVpNJrs7tZkbVaTNVB1u/8jr5i0LOli4TE6CQkSzGw243A4LsuzPOdW9VpJe/du0u9XZBXCEVCHcERW22j0pMaFmCRf5j8aTbrdCqjNji7eGzQ2jSQtopa7tvIry5ZVrbHqbrcajS6z/CL8yxf/fTz4+gO0yn9/fyuNTeOSiuIkhMM//vryE2gV83qN5+feur15c9LpHBqrg3+ml0EbNb59O2ndXr8+yfNDszqE+uPB1+zXfcxzNo3u3x+QePx4PJ16CJaSQuB8ridPxr0e53M9f37cNBYCPAkAY1J2VX/GqDxnWZ49ejSezWhGd5nR3Xd36Y7ZTGYmicCff9/Ofne+2nP44MGAxHA4ns1EmrtITqft9KBcYNuyuG5YrDQWxc1eT4CbQQKJtgfa4dPahqmTZYxR9+4N9vZu9ftsKW0bXbINoNU/87ncr/PcAHJXp8OiOH348N9v39Sir879GkoTleUsitNnz46bxkhK4lpd2jXB34IkuKOlPH16nJLRluflkpHLJG298uugEPDq1elweCyRhJIIEPr5gVze7uP6dbQeJyV8+jRNSTs7llzE1SaBwJ27N74DejPTVruTNQsAAAAldEVYdGNyZWF0ZS1kYXRlADIwMTAtMTEtMTJUMTE6MzQ6NDUtMDY6MDBeEXIgAAAAJXRFWHRtb2RpZnktZGF0ZQAyMDEwLTExLTEyVDEwOjQ2OjUyLTA2OjAw+PUmPwAAAB10RVh0U29mdHdhcmUAR1BMIEdob3N0c2NyaXB0IDguNzEDP2g0AAAAAElFTkSuQmCC""",
"nw": """iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAIAAABvFaqvAAAACXBIWXMAAAxMAAAMTAEAiU+qAAAACXZwQWcAAAAYAAAAGAB4TKWmAAACVUlEQVQ4y5WUvU4bQRSFz53ZMV7biiwewLwIRUJPjSUau+CdAIFMA/4pEWUUhPIA7FpJqkiR2yjEoDj4Z2bnpFhjjP9zitVq5u53zxntXPn5231tDwiIYKEIaCXDoddadnfzWoN8UyACRwTfvgz2PnwXQEQ4UwIBKEpE6BxPTkp77/PeQ6sFzQISSgAREsSsK6WFHkqxVitVKttJAjVHSUnpssxaGXsWehjjT09Llcq2s9R66QkEAEimXqZxIiC9MTw+Tr0wMEsYE9AiLwCQy8nZ2U65XByNaFZSAKhVewrZrKRcWcOZA6XfkBBBr8fDwx+t1qMx4hw3BnGMSCneA1DPz1KpdJrNxyAQa7kWJABECckwRD4PkkoJSaVUvy/VaqfReDRmFSsFUWuQzGRYq5UuL3fyeZBea/GeWstggKOjzpqMt3c9rWOlYmPuz88fSJK8uuqGYQTESrVfnlEYRo1Gl+Ro5PlWNiHuPv9VEmUy97XaQ1o0HHqSjUbKiqZYcRhG9foClk2Ij5/+aH1/cfFA0rnxtrWeZLPZLRQikUjrNhBr3RaJCoWo2exOal5Bt3e9k+NfaRM/1SbtWa9vlNEmxMiSpHOcV1q3PqOnTQjn6RMu0+qMrVaXpPd0nrDLKSsyisRKxZnM+HCHlgHWKf0Py+WiCKrVTr9PEUnvgDFqa+vlbqx1tChjLBIXi/HNzdN/RJs/e2OiXC6+vn6aNLDJBtFmMh4cFAcDZrOyv//O2tc5JdYzWDdrpuX9eGxPXgA4IkgIAchNQSIYOQDQGs6PVxLiH5XrpvEOYi2tAAAAJXRFWHRjcmVhdGUtZGF0ZQAyMDEwLTExLTEyVDExOjM0OjQ1LTA2OjAwXhFyIAAAACV0RVh0bW9kaWZ5LWRhdGUAMjAxMC0xMS0xMlQxMDo0NzowMS0wNjowMG4/WfgAAAAddEVYdFNvZnR3YXJlAEdQTCBHaG9zdHNjcmlwdCA4LjcxAz9oNAAAAABJRU5ErkJggg==""",
}

RAW_ICONS['leftarrow'] = RAW_ICONS['ww']
RAW_ICONS['rightarrow'] = RAW_ICONS['ee']
RAW_ICONS['uparrow'] = RAW_ICONS['nn']
RAW_ICONS['downarrow'] = RAW_ICONS['ss']


def get_icon(name):
    if name in RAW_ICONS:
        val = RAW_ICONS[name]
        if is_wxPhoenix:
            return wx.Bitmap(PyEmbeddedImage(val).GetImage())
        else:
            return wx.BitmapFromImage(PyEmbeddedImage(val).GetImage())
    return None
